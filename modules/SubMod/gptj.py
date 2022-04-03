from __future__ import annotations
from typing import Iterable
import requests

class Sentiment:
    """Advanced custom label sentiment analyzer using a GPT-J API"""

    def __init__(self, url: str = "http://api.vicgalle.net:5000"):
        """
        Initialise the sentiment analyzer

        Args:
            url: the API base URL
                ()using the one freely provided by vicgalle by default)
        """
        self.url = url

    def __call__(
        self,
        prompt: str,
        labels: Iterable[str]
    ) -> dict[str, float]:
        """
        Classify a prompt using a set of lables

        Args:
            prompt: the text to analyze
            labels: a list of labels to use.
                A label can't include commas
                (and probably some other characters too)
                (I have no idea)

        Returns:
            A dictionary where the keys are label names
            and the values are reported probabilities.
            The probabilities add up to 1
        """
        query = {"sequence": prompt, "labels": ",".join(labels)}
        route = f"{self.url}/classify"
        response = requests.post(route, params=query)
        classified = response.json()
        return {
            label: score
            for label, score in zip(classified["labels"], classified["scores"])
        }

    def multi(
        self,
        prompt: str,
        labels: Iterable[Iterable[str]]
    ) -> list[dict[str, float]]:
        """
        Classify a given prompt over a set of label groups.
        Should always be preferred over doing multiple individual
        classifications as it only performs one API call while getting
        the same results (some precision is lost but it's negligible)

        Args:
            prompt: the text to analyze
            labels: a list of lists of labels to use.
                A label can't include commas
                (and probably some other characters too)
                (I have no idea)

        Returns:
            A list of dictionaries, one per label group. The keys are label
            names and the values are probabilities. The probabilities of
            each group add up to 1.
        """
        label_set: list[str] = list(set(sum(labels, [])))
        classified: dict[str, float] = self(prompt, label_set)
        return [
            {
                label: classified[label]
                / sum(
                    value for key, value in classified.items() if key in group
                )
                for label in group
            }
            for group in labels
        ]
