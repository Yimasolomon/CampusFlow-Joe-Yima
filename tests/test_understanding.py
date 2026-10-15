import unittest

from campusflow.understanding_check import (
    QUESTIONS,
    ask_question,
    run_understanding_check,
)


class TestUnderstandingCheck(unittest.TestCase):
    def test_question_bank_has_six_questions(self):
        self.assertEqual(len(QUESTIONS), 6)

    def test_each_question_has_four_choices_and_valid_answer(self):
        for question in QUESTIONS:
            self.assertEqual(
                set(question["choices"].keys()),
                {"A", "B", "C", "D"},
            )
            self.assertIn(question["answer"], question["choices"])

    def test_invalid_answer_is_retried(self):
        answers = iter(["X", "a"])
        messages = []

        result = ask_question(
            QUESTIONS[0],
            input_fn=lambda prompt: next(answers),
            output_fn=messages.append,
        )

        self.assertEqual(result, "A")
        self.assertTrue(
            any("Invalid choice" in message for message in messages)
        )

    def test_all_correct_answers_give_six_out_of_six(self):
        inputs = []

        for question in QUESTIONS:
            inputs.append(question["answer"])

        inputs.extend(["The first reason.", "The second reason."])
        answers = iter(inputs)

        result = run_understanding_check(
            input_fn=lambda prompt: next(answers),
            output_fn=lambda message: None,
        )

        self.assertEqual(result["score"], 6)
        self.assertEqual(result["total"], 6)
        self.assertEqual(len(result["answers"]), 6)
        self.assertEqual(len(result["explanations"]), 2)

    def test_all_wrong_answers_give_zero_out_of_six(self):
        inputs = []

        for question in QUESTIONS:
            wrong_answer = next(
                choice
                for choice in ("A", "B", "C", "D")
                if choice != question["answer"]
            )
            inputs.append(wrong_answer)

        inputs.extend(["Reason one.", "Reason two."])
        answers = iter(inputs)

        result = run_understanding_check(
            input_fn=lambda prompt: next(answers),
            output_fn=lambda message: None,
        )

        self.assertEqual(result["score"], 0)
        self.assertEqual(result["total"], 6)

    def test_blank_explanation_is_rejected_and_retried(self):
        inputs = iter([
            *[question["answer"] for question in QUESTIONS],
            "",
            "First explanation.",
            "Second explanation.",
        ])
        messages = []

        result = run_understanding_check(
            input_fn=lambda prompt: next(inputs),
            output_fn=messages.append,
        )

        self.assertEqual(
            result["explanations"],
            ["First explanation.", "Second explanation."],
        )
        self.assertTrue(
            any("Please enter a short explanation." in message
                for message in messages)
        )


if __name__ == "__main__":
    unittest.main()
