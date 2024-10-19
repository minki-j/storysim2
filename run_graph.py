import uuid
import json

from graph import main_graph

from state import Scene, OpenEndedQuestion


def apply_choices(scene: Scene):
    sentence = scene.sentence
    sentence = sentence.replace(f"<blank>", scene.blank.answer)
    return sentence


def ask_reader(scenes: Scene):
    scene = scenes[-1]
    print("-" * 50)
    print(f"{scene.sentence}")
    print("\n" + "-" * 50)
    print(f"Fill in the <blank>\n{scene.blank.question}")
    user_choice = input("")
    scene.blank.answer = user_choice.strip()

    scene.completed_sentence = apply_choices(scene)

    return scene


thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 100}


main_graph.invoke(
    {
        "story": [],
    },
    config,
)

completed_sentence = input("What would be the first sentence of your story?:\n")
scene = Scene(sentence=completed_sentence, blank=OpenEndedQuestion(), completed_sentence=completed_sentence)

while True:
    main_graph.update_state(
        config,
        {
            "story": [scene],
        },
    )
    output = main_graph.invoke(None, config)
    scene = ask_reader(output["story"])
