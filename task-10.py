
class CampusIncidentSystem:

    def __init__(self):
        # Severity scores
        self.severity_scores = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }

        # Location risk scores
        self.location_scores = {
            "LABORATORY": 4,
            "HOSTEL": 3,
            "CLASSROOM": 2,
            "LIBRARY": 2,
            "CANTEEN": 2,
            "CORRIDOR": 1,
            "GARDEN": 1
        }

    def validate_incident(self, incident):
        required_fields = {
            "id", "description", "severity",
            "location", "frequency"
        }

        if not required_fields.issubset(incident):
            raise ValueError("Incident is missing required fields.")

        if not str(incident["id"]).strip():
            raise ValueError("Incident ID cannot be empty.")

        if not str(incident["description"]).strip():
            raise ValueError("Description cannot be empty.")

        severity = incident["severity"].upper()
        location = incident["location"].upper()
        frequency = incident["frequency"]

        if severity not in self.severity_scores:
            raise ValueError(
                f"Invalid severity for incident {incident['id']}."
            )

        if location not in self.location_scores:
            raise ValueError(
                f"Invalid location for incident {incident['id']}."
            )

        if (
            isinstance(frequency, bool)
            or not isinstance(frequency, int)
            or frequency < 1
        ):
            raise ValueError(
                "Frequency must be a positive integer."
            )

    def classify_incident(self, incident):
        self.validate_incident(incident)

        severity = incident["severity"].upper()
        location = incident["location"].upper()
        frequency = incident["frequency"]

        severity_score = self.severity_scores[severity]
        location_score = self.location_scores[location]

        # Frequency score increases with repeated reports.
        if frequency >= 10:
            frequency_score = 4
        elif frequency >= 5:
            frequency_score = 3
        elif frequency >= 2:
            frequency_score = 2
        else:
            frequency_score = 1

        # Weighted priority score.
        priority_score = (
            severity_score * 5
            + location_score * 3
            + frequency_score * 2
        )

        # Critical incidents always receive immediate priority.
        if severity == "CRITICAL":
            priority = "URGENT"
        elif priority_score >= 25:
            priority = "HIGH"
        elif priority_score >= 17:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        result = incident.copy()
        result.update({
            "severity": severity,
            "location": location,
            "severity_score": severity_score,
            "location_score": location_score,
            "frequency_score": frequency_score,
            "priority_score": priority_score,
            "priority": priority
        })

        return result

    def rank_incidents(self, incidents):
        classified = [
            self.classify_incident(incident)
            for incident in incidents
        ]

        # Ranking rules:
        # 1. Urgent, then high, medium, and low priority
        # 2. Higher priority score
        # 3. Greater reported frequency
        priority_order = {
            "URGENT": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }

        classified.sort(
            key=lambda incident: (
                -priority_order[incident["priority"]],
                -incident["priority_score"],
                -incident["frequency"],
                str(incident["id"])
            )
        )

        return classified

    def generate_summary(self, ranked_incidents):
        summary = {
            "total": len(ranked_incidents),
            "URGENT": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }

        for incident in ranked_incidents:
            summary[incident["priority"]] += 1

        return summary

    def display_report(self, ranked_incidents, summary):
        print("\n========== CAMPUS INCIDENT REPORT ==========")

        if not ranked_incidents:
            print("No maintenance incidents reported.")

        for rank, incident in enumerate(ranked_incidents, start=1):
            print(f"\nRank: {rank}")
            print("Incident ID:", incident["id"])
            print("Description:", incident["description"])
            print("Location:", incident["location"])
            print("Severity:", incident["severity"])
            print("Reported Frequency:", incident["frequency"])
            print("Priority Score:", incident["priority_score"])
            print("Priority Classification:", incident["priority"])

        print("\n========== PRIORITY SUMMARY ==========")
        print("Total Incidents:", summary["total"])
        print("Urgent:", summary["URGENT"])
        print("High:", summary["HIGH"])
        print("Medium:", summary["MEDIUM"])
        print("Low:", summary["LOW"])

        print("\nRecommended action:")
        if summary["URGENT"] > 0:
            print("- Address urgent incidents immediately.")
        if summary["HIGH"] > 0:
            print("- Schedule high-priority incidents promptly.")
        if summary["MEDIUM"] > 0:
            print("- Plan medium-priority maintenance.")
        if summary["LOW"] > 0:
            print("- Add low-priority cases to routine maintenance.")

        print("=======================================")


def main():
    system = CampusIncidentSystem()

    # Hypothetical maintenance reports
    incidents = [
        {
            "id": "INC101",
            "description": "Electrical sparks near laboratory equipment",
            "severity": "CRITICAL",
            "location": "LABORATORY",
            "frequency": 2
        },
        {
            "id": "INC102",
            "description": "Repeated water leakage",
            "severity": "HIGH",
            "location": "HOSTEL",
            "frequency": 7
        },
        {
            "id": "INC103",
            "description": "Broken classroom chair",
            "severity": "LOW",
            "location": "CLASSROOM",
            "frequency": 3
        },
        {
            "id": "INC104",
            "description": "Air conditioning not working",
            "severity": "MEDIUM",
            "location": "LIBRARY",
            "frequency": 5
        },
        {
            "id": "INC105",
            "description": "Damaged garden bench",
            "severity": "LOW",
            "location": "GARDEN",
            "frequency": 1
        }
    ]

    try:
        ranked_incidents = system.rank_incidents(incidents)
        summary = system.generate_summary(ranked_incidents)
        system.display_report(ranked_incidents, summary)

    except ValueError as error:
        print("Validation Error:", error)


if __name__ == "__main__":
    main()
