import numpy as np

def sort_attributes(attributes):
    parameters = parameter_schema.copy()

    parameters["deep_hang"] = attributes["deep_hang"]
    parameters["shallow_hang"] = attributes["shallow_hang"]
    parameters["no_hang"] = attributes["no_hang"]
    parameters["auto_leave"] = attributes["auto_leave"]

    if "auto_1" in attributes["starting_clusters"]:
        parameters["auto_1"] = attributes["starting_clusters"]["auto_1"]
    if "auto_2" in attributes["starting_clusters"]:
        parameters["auto_2"] = attributes["starting_clusters"]["auto_2"]
    if "auto_3" in attributes["starting_clusters"]:
        parameters["auto_3"] = attributes["starting_clusters"]["auto_3"]

    parameters["auto_algae_remover"] = attributes["phases"]["auto"]["algae_remover"]

    parameters["auto_reef_frequency"] = attributes["phases"]["auto"]["place"]["reef"]["frequency"]
    parameters["auto_reef_accuracy"] = attributes["phases"]["auto"]["place"]["reef"]["accuracy"]
    parameters["auto_reef_ability"] = attributes["phases"]["auto"]["place"]["reef"]["ability"]

    parameters["auto_l1_frequency"] = attributes["phases"]["auto"]["place"]["l1"]["frequency"]
    parameters["auto_l1_accuracy"] = attributes["phases"]["auto"]["place"]["l1"]["accuracy"]
    parameters["auto_l1_ability"] = attributes["phases"]["auto"]["place"]["l1"]["ability"]

    parameters["auto_l2_frequency"] = attributes["phases"]["auto"]["place"]["l2"]["frequency"]
    parameters["auto_l2_accuracy"] = attributes["phases"]["auto"]["place"]["l2"]["accuracy"]
    parameters["auto_l2_ability"] = attributes["phases"]["auto"]["place"]["l2"]["ability"]

    parameters["auto_l3_frequency"] = attributes["phases"]["auto"]["place"]["l3"]["frequency"]
    parameters["auto_l3_accuracy"] = attributes["phases"]["auto"]["place"]["l3"]["accuracy"]
    parameters["auto_l3_ability"] = attributes["phases"]["auto"]["place"]["l3"]["ability"]

    parameters["auto_l4_frequency"] = attributes["phases"]["auto"]["place"]["l4"]["frequency"]
    parameters["auto_l4_accuracy"] = attributes["phases"]["auto"]["place"]["l4"]["accuracy"]
    parameters["auto_l4_ability"] = attributes["phases"]["auto"]["place"]["l4"]["ability"]

    parameters["auto_barge_frequency"] = attributes["phases"]["auto"]["place"]["barge"]["frequency"]
    parameters["auto_barge_accuracy"] = attributes["phases"]["auto"]["place"]["barge"]["accuracy"]
    parameters["auto_barge_ability"] = attributes["phases"]["auto"]["place"]["barge"]["ability"]

    parameters["auto_processor_frequency"] = attributes["phases"]["auto"]["place"]["processor"]["frequency"]
    parameters["auto_processor_accuracy"] = attributes["phases"]["auto"]["place"]["processor"]["accuracy"]
    parameters["auto_processor_ability"] = attributes["phases"]["auto"]["place"]["processor"]["ability"]

    parameters["tele_algae_remover"] = attributes["phases"]["teleOp"]["algae_remover"]

    parameters["tele_reef_frequency"] = attributes["phases"]["teleOp"]["place"]["reef"]["frequency"]
    parameters["tele_reef_accuracy"] = attributes["phases"]["teleOp"]["place"]["reef"]["accuracy"]
    parameters["tele_reef_ability"] = attributes["phases"]["teleOp"]["place"]["reef"]["ability"]

    parameters["tele_l1_frequency"] = attributes["phases"]["teleOp"]["place"]["l1"]["frequency"]
    parameters["tele_l1_accuracy"] = attributes["phases"]["teleOp"]["place"]["l1"]["accuracy"]
    parameters["tele_l1_ability"] = attributes["phases"]["teleOp"]["place"]["l1"]["ability"]

    parameters["tele_l2_frequency"] = attributes["phases"]["teleOp"]["place"]["l2"]["frequency"]
    parameters["tele_l2_accuracy"] = attributes["phases"]["teleOp"]["place"]["l2"]["accuracy"]
    parameters["tele_l2_ability"] = attributes["phases"]["teleOp"]["place"]["l2"]["ability"]

    parameters["tele_l3_frequency"] = attributes["phases"]["teleOp"]["place"]["l3"]["frequency"]
    parameters["tele_l3_accuracy"] = attributes["phases"]["teleOp"]["place"]["l3"]["accuracy"]
    parameters["tele_l3_ability"] = attributes["phases"]["teleOp"]["place"]["l3"]["ability"]

    parameters["tele_l4_frequency"] = attributes["phases"]["teleOp"]["place"]["l4"]["frequency"]
    parameters["tele_l4_accuracy"] = attributes["phases"]["teleOp"]["place"]["l4"]["accuracy"]
    parameters["tele_l4_ability"] = attributes["phases"]["teleOp"]["place"]["l4"]["ability"]

    parameters["tele_barge_frequency"] = attributes["phases"]["teleOp"]["place"]["barge"]["frequency"]
    parameters["tele_barge_accuracy"] = attributes["phases"]["teleOp"]["place"]["barge"]["accuracy"]
    parameters["tele_barge_ability"] = attributes["phases"]["teleOp"]["place"]["barge"]["ability"]

    parameters["tele_processor_frequency"] = attributes["phases"]["teleOp"]["place"]["processor"]["frequency"]
    parameters["tele_processor_accuracy"] = attributes["phases"]["teleOp"]["place"]["processor"]["accuracy"]
    parameters["tele_processor_ability"] = attributes["phases"]["teleOp"]["place"]["processor"]["ability"]

    return np.array([parameters[key] for key in parameter_order], dtype=np.float32).reshape(1, -1)

parameter_schema = {
    "deep_hang": -1,
    "shallow_hang": -1,
    "no_hang": 1,
    "auto_leave": -1,

    "auto_1": -1,
    "auto_2": -1,
    "auto_3": -1,

    "auto_algae_remover": -1,

    "auto_reef_frequency": 0,
    "auto_reef_accuracy": 0,
    "auto_reef_ability": -1,

    "auto_l1_frequency": 0,
    "auto_l1_accuracy": 0,
    "auto_l1_ability": -1,

    "auto_l2_frequency": 0,
    "auto_l2_accuracy": 0,
    "auto_l2_ability": -1,

    "auto_l3_frequency": 0,
    "auto_l3_accuracy": 0,
    "auto_l3_ability": -1,

    "auto_l4_frequency": 0,
    "auto_l4_accuracy": 0,
    "auto_l4_ability": -1,

    "auto_barge_frequency": 0,
    "auto_barge_accuracy": 0,
    "auto_barge_ability": -1,

    "auto_processor_frequency": 0,
    "auto_processor_accuracy": 0,
    "auto_processor_ability": -1,

    "tele_algae_remover": -1,

    "tele_reef_frequency": 0,
    "tele_reef_accuracy": 0,
    "tele_reef_ability": -1,

    "tele_l1_frequency": 0,
    "tele_l1_accuracy": 0,

    "tele_l2_frequency": 0,
    "tele_l2_accuracy": 0,
    "tele_l2_ability": -1,

    "tele_l3_frequency": 0,
    "tele_l3_accuracy": 0,
    "tele_l3_ability": -1,

    "tele_l4_frequency": 0,
    "tele_l4_accuracy": 0,
    "tele_l4_ability": -1,

    "tele_barge_frequency": 0,
    "tele_barge_accuracy": 0,
    "tele_barge_ability": -1,

    "tele_processor_frequency": 0,
    "tele_processor_accuracy": 0,
    "tele_processor_ability": -1,
}

parameter_order = [
    "deep_hang",
    "shallow_hang",
    "no_hang",
    "auto_leave",
    "auto_1",
    "auto_2",
    "auto_3",
    "auto_algae_remover",
    "auto_reef_frequency",
    "auto_reef_accuracy",
    "auto_reef_ability",
    "auto_l1_frequency",
    "auto_l1_accuracy",
    "auto_l1_ability",
    "auto_l2_frequency",
    "auto_l2_accuracy",
    "auto_l2_ability",
    "auto_l3_frequency",
    "auto_l3_accuracy",
    "auto_l3_ability",
    "auto_l4_frequency",
    "auto_l4_accuracy",
    "auto_l4_ability",
    "auto_barge_frequency",
    "auto_barge_accuracy",
    "auto_barge_ability",
    "auto_processor_frequency",
    "auto_processor_accuracy",
    "auto_processor_ability",
    "tele_algae_remover",
    "tele_reef_frequency",
    "tele_reef_accuracy",
    "tele_reef_ability",
    "tele_l1_frequency",
    "tele_l1_accuracy",
    "tele_l2_frequency",
    "tele_l2_accuracy",
    "tele_l2_ability",
    "tele_l3_frequency",
    "tele_l3_accuracy",
    "tele_l3_ability",
    "tele_l4_frequency",
    "tele_l4_accuracy",
    "tele_l4_ability",
    "tele_barge_frequency",
    "tele_barge_accuracy",
    "tele_barge_ability",
    "tele_processor_frequency",
    "tele_processor_accuracy",
    "tele_processor_ability"
]

attribute_schema = {
    "deep_hang": -1,
    "shallow_hang": -1,
    "no_hang": 1,
    "auto_leave": -1,
    "starting_clusters": None,
    "phases": {
        "auto": {
            "algae_remover": -1,
            "place": {
                "reef": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                },
                "l1": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                },
                "l2": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                },
                "l3": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                },
                "l4": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                },
                "barge": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                },
                "processor": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                }
            }
        },
        "teleOp": {
            "algae_remover": -1,
            "place": {
                "reef": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                },
                "l1": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                },
                "l2": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                },
                "l3": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                },
                "l4": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                },
                "barge": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                },
                "processor": {
                    "score": 0,
                    "miss": 0,
                    "frequency": 0,
                    "accuracy": 0,
                    "ability": -1
                }
            }
        }
    }
}