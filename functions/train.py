import tensorflow as tf

from functions.schema import parameter_order


class Trainer:
    def __init__(self, model, optimizer, teams):
        self.model = model
        self.optimizer = optimizer
        self.teams = teams

    def train(self, epochs):
        for epoch in range(epochs):
            epoch_loss = 0
            for i, team in enumerate(self.teams):
                loss = self.train_step(team)
                epoch_loss += loss

                if (i + 1) % 10 == 0:  # Print every 10 teams
                    print(f"Epoch {epoch + 1}, Team {i + 1}/{len(self.teams)}, Loss: {loss:.4f}")

            avg_loss = epoch_loss / len(self.teams)
            print(f"Epoch {epoch + 1} completed - Average Loss: {avg_loss:.4f}\n")

    def train_step(self, team):
        with tf.GradientTape() as tape:
            self.model.create_parameters(team)

            archetype_a, archetype_b = self.model.predict()

            loss = self.compute_loss(archetype_a, archetype_b)

        gradients = tape.gradient(loss, self.model.model.trainable_variables)

        if gradients is None or all(g is None for g in gradients):
            print("WARNING: No gradients computed!")
            print(f"Trainable variables: {len(self.model.model.trainable_variables)}")
            return 0.0

        gradients, _ = tf.clip_by_global_norm(gradients, 1.0)

        self.optimizer.apply_gradients(
            zip(gradients, self.model.model.trainable_variables)
        )

        return loss.numpy()

    def compute_loss(self, archetype_a, archetype_b):
        team = self.model.parameters
        reward = self.compute_reward(archetype_a, archetype_b, team)

        # Add regularization to prevent extreme predictions
        # Penalize predictions that are too far from reasonable ranges
        reg_loss = tf.reduce_mean(tf.square(archetype_a)) + tf.reduce_mean(tf.square(archetype_b))

        # Negative reward (we minimize loss = maximize reward)
        # But scale it down and add regularization
        loss = -reward * 0.01 + reg_loss * 0.1

        return loss

    def compute_reward(self, archetype_a, archetype_b, team):
        """
        TensorFlow-compatible reward computation with normalized values
        """
        reward = tf.constant(0.0, dtype=tf.float32)

        arch_a = tf.reshape(archetype_a, [-1])
        arch_b = tf.reshape(archetype_b, [-1])
        team_params = tf.reshape(team, [-1])

        # Normalize predictions to [-1, 1] range using tanh
        arch_a = tf.tanh(arch_a)
        arch_b = tf.tanh(arch_b)

        robots = tf.stack([team_params, arch_a, arch_b], axis=0)

        def get_idx(param_name):
            return parameter_order.index(param_name)

        # ============================================================
        # AUTO REWARDS (scaled down)
        # ============================================================

        auto_reef_idx = get_idx('auto_reef_frequency')
        auto_barge_idx = get_idx('auto_barge_frequency')

        auto_reef_total = tf.reduce_sum(tf.nn.relu(robots[:, auto_reef_idx]))
        auto_barge_total = tf.reduce_sum(tf.nn.relu(robots[:, auto_barge_idx]))

        reward += auto_reef_total * 1.5  # Scaled down from 15
        reward += auto_barge_total * 1.0  # Scaled down from 10

        # Auto Level Coverage
        auto_level_indices = [
            get_idx('auto_l1_frequency'),
            get_idx('auto_l2_frequency'),
            get_idx('auto_l3_frequency'),
            get_idx('auto_l4_frequency')
        ]

        for idx in auto_level_indices:
            max_freq = tf.reduce_max(robots[:, idx])
            reward += tf.nn.relu(max_freq - 0.3) * 0.5

        # Auto Accuracy Bonus
        auto_accuracy_indices = [
            get_idx('auto_reef_accuracy'),
            get_idx('auto_l1_accuracy'),
            get_idx('auto_l2_accuracy'),
            get_idx('auto_l3_accuracy'),
            get_idx('auto_l4_accuracy'),
            get_idx('auto_barge_accuracy')
        ]

        for idx in auto_accuracy_indices:
            avg_accuracy = tf.reduce_mean(robots[:, idx])
            reward += tf.nn.relu(avg_accuracy - 0.7) * 0.8

        # ============================================================
        # TELEOP REWARDS (scaled down)
        # ============================================================

        tele_reef_idx = get_idx('tele_reef_frequency')
        tele_barge_idx = get_idx('tele_barge_frequency')

        tele_reef_total = tf.reduce_sum(tf.nn.relu(robots[:, tele_reef_idx]))
        tele_barge_total = tf.reduce_sum(tf.nn.relu(robots[:, tele_barge_idx]))

        reward += tele_reef_total * 2.0  # Scaled down from 20
        reward += tele_barge_total * 1.5  # Scaled down from 15

        # ============================================================
        # ENDGAME REWARDS (scaled down)
        # ============================================================

        deep_hang_idx = get_idx('deep_hang')
        shallow_hang_idx = get_idx('shallow_hang')

        deep_hangs = tf.reduce_sum(tf.cast(robots[:, deep_hang_idx] > 0, tf.float32))
        shallow_hangs = tf.reduce_sum(tf.cast(robots[:, shallow_hang_idx] > 0, tf.float32))
        total_hangs = deep_hangs + shallow_hangs

        reward += deep_hangs * 2.5  # Scaled down from 25
        reward += shallow_hangs * 1.2  # Scaled down from 12

        reward += tf.nn.relu(total_hangs - 1.5) * 1.5
        reward += tf.nn.relu(total_hangs - 2.5) * 2.0

        # ============================================================
        # STRATEGIC BONUSES (scaled down)
        # ============================================================

        reef_freqs = robots[:, auto_reef_idx] + robots[:, tele_reef_idx]
        barge_freqs = robots[:, auto_barge_idx] + robots[:, tele_barge_idx]

        reef_diversity = tf.reduce_max(reef_freqs) - tf.reduce_min(reef_freqs)
        barge_diversity = tf.reduce_max(barge_freqs) - tf.reduce_min(barge_freqs)

        reward += (reef_diversity + barge_diversity) * 0.5

        # Penalties (scaled down)
        critical_indices = [auto_reef_idx, tele_reef_idx, auto_barge_idx, tele_barge_idx]

        for idx in critical_indices:
            max_capability = tf.reduce_max(robots[:, idx])
            reward -= tf.nn.relu(0.1 - max_capability) * 2.0  # Scaled down from 200

        return reward