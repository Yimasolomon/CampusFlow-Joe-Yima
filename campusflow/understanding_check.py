QUESTIONS = [
    {
        "question": (
            "An open, unassigned ticket must move to in_progress. "
            "What should happen?"
        ),
        "choices": {
            "A": "Accept the valid status transition",
            "B": "Reject and preserve all data",
            "C": "Resolve the ticket automatically",
            "D": "Remove the ticket",
        },
        "answer": "A",
    },
    {
        "question": "What is the resolution percentage with zero tickets?",
        "choices": {
            "A": "Crash",
            "B": "100%",
            "C": "0%",
            "D": "Divide by one without explanation",
        },
        "answer": "C",
    },
    {
        "question": (
            "A search specifies title='wifi', category='Network', "
            "and status='open'. Which tickets should match?"
        ),
        "choices": {
            "A": "Any ticket matching at least one filter",
            "B": "Only tickets matching every supplied filter",
            "C": "All Network tickets",
            "D": "All open tickets",
        },
        "answer": "B",
    },
    {
        "question": "What happens when someone adds a note to a resolved ticket?",
        "choices": {
            "A": "Append the note anyway",
            "B": "Delete existing notes",
            "C": "Reject the note until the ticket is reopened",
            "D": "Silently change the ticket status",
        },
        "answer": "C",
    },
    {
        "question": "A JSON file contains duplicate ticket IDs. What should happen?",
        "choices": {
            "A": "Keep both tickets",
            "B": "Replace memory with the duplicate records",
            "C": "Reject the load and preserve current memory",
            "D": "Rename IDs silently",
        },
        "answer": "C",
    },
    {
        "question": (
            "A pull request changes validation but adds no negative-case "
            "tests. What is the best review action?"
        ),
        "choices": {
            "A": "Approve because the code runs",
            "B": "Request focused tests and an explanation of the reasoning",
            "C": "Merge immediately",
            "D": "Ask AI to approve it",
        },
        "answer": "B",
    },
]


def ask_question(question, input_fn=input, output_fn=print):
    """Ask one question and retry until A, B, C, or D is entered."""
    output_fn("")
    output_fn(question["question"])

    for letter, choice_text in question["choices"].items():
        output_fn(f"{letter}. {choice_text}")

    while True:
        answer = input_fn("Your answer (A/B/C/D): ").strip().upper()

        if answer in question["choices"]:
            return answer

        output_fn("Invalid choice. Enter A, B, C, or D.")


def run_understanding_check(input_fn=input, output_fn=print):
    """Run the quiz, calculate the score, and collect two explanations."""
    score = 0
    answers = []

    output_fn("\n=== Engineering Understanding Check ===")
    output_fn("Answer six questions. Each correct answer earns one point.")

    for index, question in enumerate(QUESTIONS, start=1):
        output_fn(f"\nQuestion {index} of {len(QUESTIONS)}")
        answer = ask_question(question, input_fn, output_fn)
        correct = answer == question["answer"]

        if correct:
            score += 1
            output_fn("Correct.")
        else:
            output_fn(
                f"Not quite. The correct answer is {question['answer']}."
            )

        answers.append(
            {
                "question": question["question"],
                "answer": answer,
                "correct_answer": question["answer"],
                "correct": correct,
            }
        )

    output_fn(f"\nFinal score: {score}/{len(QUESTIONS)}")

    explanations = []
    for number in range(1, 3):
        while True:
            explanation = input_fn(
                f"Explain the reasoning behind one of your answers "
                f"({number} of 2): "
            ).strip()

            if explanation:
                explanations.append(explanation)
                break

            output_fn("Please enter a short explanation.")

    output_fn("\nQuiz complete. Keep your explanations for mentor discussion.")

    return {
        "score": score,
        "total": len(QUESTIONS),
        "answers": answers,
        "explanations": explanations,
    }
