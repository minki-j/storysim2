import uuid
import json

from graph import main_graph

from state import Scene, MultipleChoiceQuestion, OpenEndedQuestion, Option


def ask_reader(scenes: Scene):
    scene = scenes[-1]
    option_setence = ""
    option_setence += "-" * 30 + "\n"
    for i, question in enumerate(scene.questions):
        option_setence += f"Q {question.question}\n"
        if isinstance(question, MultipleChoiceQuestion):
            for j, option in enumerate(question.options):
                option_setence += f"{j+1}. {(option.content)}\n"
        option_setence += "-" * 30 + "\n"
    print("#" * 30)
    print(
        f"Complete the sentence using the following options:\nSentence: {scene.sentence}\n{option_setence}"
    )
    print("#" * 30)
    for i, question in enumerate(scene.questions):
        if isinstance(question, MultipleChoiceQuestion):
            user_choice = input(
                f"Enter the number of the choice for {question.question}:"
            )
            try:
                user_choice_int = int(user_choice)
                scene.questions[i].options[user_choice_int-1].chosen = True
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
                continue
        elif isinstance(question, OpenEndedQuestion):
            user_choice = input(
                f"Enter the answer for {question.question}:"
            )
            scene.questions[i].answer = user_choice
    return scene


thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": 24}, "recursion_limit": 100}


seed_scenes = [Scene(
    sentence="It was a rainy day in the <blank1> of <blank2>.",
    questions=[
        MultipleChoiceQuestion(
            question="city or town?",
            options=[
                Option(content="city"),
                Option(content="town"),
            ],
        ),
        OpenEndedQuestion(question="name of the city or town?", answer=""),
    ],
)]


main_graph.invoke(
    {
        "story": [],
    },
    config,
)
scene = ask_reader(seed_scenes)

while True:

    main_graph.update_state(
        config,
        {
            "story": [scene],
        },
    )
    output = main_graph.invoke(None, config)
    scene = ask_reader(output["story"])
