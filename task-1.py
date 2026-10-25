
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional


# -------------------------------
# Payment Policy
# -------------------------------

@dataclass
class PaymentPolicy:
    senior_discount_percent: Decimal = Decimal("10")
    insurance_discount_percent: Decimal = Decimal("5")
    low_income_discount_percent: Decimal = Decimal("15")
    concession_limit: Decimal = Decimal("30")
    low_income_threshold: Decimal = Decimal("10000")
    tax_percent: Decimal = Decimal("0")

    # Example classification thresholds
    subsidized_threshold: Decimal = Decimal("5000")


# -------------------------------
# Patient Details
# -------------------------------

@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    patient_type: str  # SELF_PAY, INSURED, GOVERNMENT
    income: Decimal
    consultation_charge: Decimal
    diagnostic_charge: Decimal
    treatment_charge: Decimal
    payment_made: Decimal = Decimal("0")
    is_low_income: bool = False


# -------------------------------
# Billing System
# -------------------------------

class HospitalBilling:

    VALID_PATIENT_TYPES = {
        "SELF_PAY", "INSURED", "GOVERNMENT"
    }

    def __init__(self, policy: PaymentPolicy):
        self.policy = policy

    @staticmethod
    def money(value: Decimal) -> Decimal:
        return value.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

    def validate(self, patient: Patient) -> None:
        if not patient.patient_id.strip():
            raise ValueError("Patient ID is required.")

        if not patient.name.strip():
            raise ValueError("Patient name is required.")

        if patient.age < 0 or patient.age > 125:
            raise ValueError("Invalid patient age.")

        if patient.patient_type not in self.VALID_PATIENT_TYPES:
            raise ValueError("Invalid patient payment type.")

        charges = [
            patient.consultation_charge,
            patient.diagnostic_charge,
            patient.treatment_charge,
            patient.payment_made,
            patient.income,
        ]

        if any(amount < 0 for amount in charges):
            raise ValueError(
                "Charges, payment, and income cannot be negative."
            )

        if self.policy.concession_limit < 0 or (
            self.policy.concession_limit > 100
        ):
            raise ValueError(
                "Concession limit must be between 0 and 100."
            )

        if self.policy.tax_percent < 0:
            raise ValueError("Tax rate cannot be negative.")

        discount_rates = [
            self.policy.senior_discount_percent,
            self.policy.insurance_discount_percent,
            self.policy.low_income_discount_percent,
        ]

        if any(rate < 0 or rate > 100 for rate in discount_rates):
            raise ValueError(
                "Discount percentages must be between 0 and 100."
            )

    def calculate_bill(self, patient: Patient) -> dict:
        self.validate(patient)

        consultation = self.money(patient.consultation_charge)
        diagnostics = self.money(patient.diagnostic_charge)
        treatment = self.money(patient.treatment_charge)

        gross = self.money(
            consultation + diagnostics + treatment
        )

        # Apply eligible concessions.
        # This example adds eligible rates, then applies a cap.
        discount_rate = Decimal("0")

        if patient.age >= 60:
            discount_rate += (
                self.policy.senior_discount_percent
            )

        if patient.patient_type == "INSURED":
            discount_rate += (
                self.policy.insurance_discount_percent
            )

        if (
            patient.is_low_income
            and patient.income
            <= self.policy.low_income_threshold
        ):
            discount_rate += (
                self.policy.low_income_discount_percent
            )

        discount_rate = min(
            discount_rate,
            self.policy.concession_limit
        )

        concession = self.money(
            gross * discount_rate / Decimal("100")
        )

        # Government-sponsored patients are exempt from
        # charges in this illustrative policy.
        # Replace this rule if the supplied policy differs.
        if patient.patient_type == "GOVERNMENT":
            concession = gross

        taxable_amount = gross - concession

        tax = self.money(
            taxable_amount
            * self.policy.tax_percent
            / Decimal("100")
        )

        net_bill = self.money(taxable_amount + tax)

        if patient.payment_made > net_bill:
            raise ValueError(
                "Payment cannot exceed the final bill."
            )

        balance = self.money(net_bill - patient.payment_made)

        classification = self.classify_patient(
            patient, balance
        )

        return {
            "patient_id": patient.patient_id,
            "patient_name": patient.name,
            "patient_type": patient.patient_type,
            "consultation_charge": consultation,
            "diagnostic_charge": diagnostics,
            "treatment_charge": treatment,
            "gross_total": gross,
            "concession_percent": discount_rate,
            "concession_amount": concession,
            "tax_amount": tax,
            "net_bill": net_bill,
            "payment_made": patient.payment_made,
            "outstanding_balance": balance,
            "payment_status": (
                "PAID" if balance == 0 else "PENDING"
            ),
            "classification": classification,
        }

    def classify_patient(
        self, patient: Patient, balance: Decimal
    ) -> str:
        if patient.patient_type == "GOVERNMENT":
            return "GOVERNMENT_SPONSORED"

        if patient.patient_type == "INSURED":
            return "INSURED_PATIENT"

        if (
            patient.is_low_income
            and patient.income
            <= self.policy.low_income_threshold
        ):
            return "SUBSIDIZED_PATIENT"

        if balance > self.policy.subsidized_threshold:
            return "HIGH_BALANCE_SELF_PAY"

        return "STANDARD_SELF_PAY"


# -------------------------------
# Example Execution
# -------------------------------

if __name__ == "__main__":
    policy = PaymentPolicy(
        senior_discount_percent=Decimal("10"),
        insurance_discount_percent=Decimal("5"),
        low_income_discount_percent=Decimal("15"),
        concession_limit=Decimal("30"),
        low_income_threshold=Decimal("10000"),
        tax_percent=Decimal("0"),
        subsidized_threshold=Decimal("5000"),
    )

    billing_system = HospitalBilling(policy)

    patient = Patient(
        patient_id="P1001",
        name="Example Patient",
        age=65,
        patient_type="INSURED",
        income=Decimal("8000"),
        consultation_charge=Decimal("500"),
        diagnostic_charge=Decimal("1500"),
        treatment_charge=Decimal("6000"),
        payment_made=Decimal("1000"),
        is_low_income=True,
    )

    try:
        bill = billing_system.calculate_bill(patient)

        print("\n===== HOSPITAL BILL =====")
        for key, value in bill.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    except ValueError as error:
        print("Billing validation failed:", error)
