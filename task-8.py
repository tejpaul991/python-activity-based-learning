
from statistics import mean, pstdev


class SportsPerformanceAnalysis:

    def __init__(self, player_scores):
        """
        player_scores format:
        {
            "Player A": [50, 60, 70],
            "Player B": [80, 75, 85]
        }
        """
        self.player_scores = player_scores
        self.validate_data()

    def validate_data(self):
        if not self.player_scores:
            raise ValueError("At least one player is required.")

        expected_matches = None

        for player, scores in self.player_scores.items():
            if not player.strip():
                raise ValueError("Player name cannot be empty.")

            if not isinstance(scores, list) or not scores:
                raise ValueError(
                    f"{player} must have a non-empty list of scores."
                )

            if expected_matches is None:
                expected_matches = len(scores)
            elif len(scores) != expected_matches:
                raise ValueError(
                    "All players must have the same number of matches."
                )

            for score in scores:
                if (
                    isinstance(score, bool)
                    or not isinstance(score, (int, float))
                    or score < 0
                ):
                    raise ValueError(
                        f"Invalid score for {player}: {score}"
                    )

    def calculate_statistics(self, scores):
        average_score = mean(scores)
        consistency = pstdev(scores)

        if len(scores) == 1:
            trend = "INSUFFICIENT DATA"
        elif scores[-1] > scores[0]:
            trend = "IMPROVING"
        elif scores[-1] < scores[0]:
            trend = "DECLINING"
        else:
            trend = "STABLE"

        return {
            "scores": scores,
            "total": sum(scores),
            "average": round(average_score, 2),
            "highest": max(scores),
            "lowest": min(scores),
            "consistency": round(consistency, 2),
            "trend": trend
        }

    def analyse(self):
        results = {}

        for player, scores in self.player_scores.items():
            results[player] = self.calculate_statistics(scores)

        return results

    def rank_players(self):
        results = self.analyse()

        # Ranking rules:
        # 1. Highest total score
        # 2. Highest average score
        # 3. Lowest population standard deviation
        # 4. Highest single-match score
        ranked_players = sorted(
            results.items(),
            key=lambda item: (
                -item[1]["total"],
                -item[1]["average"],
                item[1]["consistency"],
                -item[1]["highest"]
            )
        )

        return ranked_players

    def display_report(self):
        results = self.analyse()
        ranking = self.rank_players()

        print("\n========== PLAYER PERFORMANCE ANALYSIS ==========")

        for player, stats in results.items():
            print(f"\nPlayer: {player}")
            print("Match Scores:", stats["scores"])
            print("Total Score:", stats["total"])
            print("Average Score:", stats["average"])
            print("Highest Score:", stats["highest"])
            print("Lowest Score:", stats["lowest"])
            print("Score Standard Deviation:", stats["consistency"])
            print("Performance Trend:", stats["trend"])

        print("\n================ PLAYER RANKING =================")

        for position, (player, stats) in enumerate(ranking, start=1):
            print(
                f"{position}. {player} | "
                f"Total: {stats['total']} | "
                f"Average: {stats['average']} | "
                f"Consistency SD: {stats['consistency']} | "
                f"Trend: {stats['trend']}"
            )

        print("==================================================")


def main():
    try:
        player_scores = {}

        number_of_players = int(input("Enter number of players: "))

        if number_of_players <= 0:
            raise ValueError("Number of players must be positive.")

        for i in range(number_of_players):
            name = input(f"\nEnter player {i + 1} name: ").strip()

            if not name:
                raise ValueError("Player name cannot be empty.")

            if name in player_scores:
                raise ValueError("Player names must be unique.")

            scores_text = input(
                f"Enter scores for {name}, separated by spaces: "
            )

            scores = [float(value) for value in scores_text.split()]

            player_scores[name] = scores

        analysis = SportsPerformanceAnalysis(player_scores)
        analysis.display_report()

    except ValueError as error:
        print("Input Error:", error)


if __name__ == "__main__":
    main()
