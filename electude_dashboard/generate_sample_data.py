"""
Sample Data Generator for Electude Africa Dashboard
Creates realistic sample data for demonstration and testing purposes.
"""

import pandas as pd
import numpy as np
from typing import List, Dict
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# African countries in the Electude network
COUNTRIES = [
    "Kenya", "Uganda", "Tanzania", "Rwanda", "Ethiopia",
    "Ghana", "Nigeria", "South Africa", "Zambia", "Malawi"
]

# Languages used in African TVET institutions
LANGUAGES = ["English", "French", "Swahili", "Portuguese", "Arabic"]

# Institution name templates
INSTITUTION_TEMPLATES = [
    "{country} Technical Training College",
    "{country} Institute of Technology",
    "{country} TVET Academy",
    "{country} Vocational Training Center",
    "{country} Technical Institute",
    "{country} Polytechnic College",
    "{country} Skills Development Centre",
    "{country} Engineering Institute"
]

# Teacher name components
FIRST_NAMES = [
    "James", "Mary", "John", "Sarah", "Peter", "Grace", "David", "Ruth",
    "Michael", "Esther", "Daniel", "Elizabeth", "Joseph", "Faith", "Samuel",
    "Ann", "Paul", "Margaret", "Andrew", "Jane", "Robert", "Agnes", "William",
    "Beatrice", "Richard", "Catherine", "Thomas", "Dorothy", "Charles", "Helen"
]

LAST_NAMES = [
    "Ochieng", "Kamau", "Njoroge", "Wanjiku", "Muthoni", "Kipchoge", "Keter",
    "Mwangi", "Otieno", "Wambui", "Kimani", "Akinyi", "Ndungu", "Achieng",
    "Musyoka", "Ndlovu", "Dlamini", "Mokoena", "Nkosi", "Zulu", "Molefe",
    "Mensah", "Owusu", "Asante", "Agyeman", "Boateng", "Addo", "Annor"
]

# Electude domains
ELECTUDE_DOMAINS = [
    "Automotive Technology",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Renewable Energy",
    "Digital Electronics",
    "Hydraulic Systems",
    "Engine Management",
    "Vehicle Diagnostics"
]

# Sample feedback templates
POSITIVE_FEEDBACK = [
    "Excellent platform with comprehensive learning materials.",
    "Very satisfied with the hands-on simulations.",
    "Great improvement in practical skills among students.",
    "The interactive modules keep students engaged.",
    "Highly recommend for technical training.",
    "Outstanding support from the Electude team.",
    "Students show remarkable progress in diagnostics.",
    "Best investment for our automotive department."
]

NEGATIVE_FEEDBACK = [
    "Would benefit from more local language support.",
    "Internet connectivity challenges in rural areas.",
    "Need more advanced modules for senior students.",
    "Request for mobile-friendly interface.",
    "Would like to see more African vehicle models."
]

NEUTRAL_FEEDBACK = [
    "Good platform overall, some minor improvements needed.",
    "Students find it helpful but suggest more practice tests.",
    "Average experience, could use more features.",
    "Meeting expectations for basic training needs."
]


def generate_teacher_name() -> str:
    """Generate a realistic African teacher name."""
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def generate_email(name: str, institution: str) -> str:
    """Generate a professional email address."""
    parts = name.lower().split()
    inst_short = institution.split()[0].lower()
    domains = ["gmail.com", "yahoo.com", "outlook.com", f"{inst_short}.ac.africa"]
    return f"{parts[0]}.{parts[1]}@{random.choice(domains)}"


def generate_phone(country: str) -> str:
    """Generate a realistic phone number for the country."""
    country_codes = {
        "Kenya": "+254", "Uganda": "+256", "Tanzania": "+255",
        "Rwanda": "+250", "Ethiopia": "+251", "Ghana": "+233",
        "Nigeria": "+234", "South Africa": "+27", "Zambia": "+260",
        "Malawi": "+265"
    }
    code = country_codes.get(country, "+254")
    number = "".join([str(random.randint(0, 9)) for _ in range(9)])
    return f"{code} {number[:3]} {number[3:6]} {number[6:]}"


def generate_institution_name(country: str) -> str:
    """Generate a realistic institution name."""
    template = random.choice(INSTITUTION_TEMPLATES)
    return template.format(country=country)


def generate_feedback(satisfaction_score: float) -> str:
    """Generate feedback based on satisfaction score."""
    if satisfaction_score >= 4:
        return random.choice(POSITIVE_FEEDBACK)
    elif satisfaction_score >= 3:
        return random.choice(NEUTRAL_FEEDBACK)
    else:
        return random.choice(NEGATIVE_FEEDBACK)


def generate_main_data(n_records: int = 500) -> pd.DataFrame:
    """
    Generate the main dataset with realistic TVET institution data.
    
    Args:
        n_records: Number of records to generate
        
    Returns:
        DataFrame with main data
    """
    records = []
    
    # Generate institutions
    institutions = {}
    for country in COUNTRIES:
        # 2-5 institutions per country
        n_institutions = random.randint(2, 5)
        for _ in range(n_institutions):
            inst_name = generate_institution_name(country)
            institutions[inst_name] = {
                "country": country,
                "language": random.choice(LANGUAGES),
                "domain": random.choice(ELECTUDE_DOMAINS)
            }
    
    # Generate records
    for _ in range(n_records):
        institution = random.choice(list(institutions.keys()))
        inst_data = institutions[institution]
        teacher_name = generate_teacher_name()
        
        record = {
            "Institution": f"{institution} - {inst_data['country']}",
            "Teacher / Trainer": teacher_name,
            "Number of Students": random.randint(10, 200),
            "EMAIL": generate_email(teacher_name, institution),
            "Phone number": generate_phone(inst_data["country"]),
            "Language": inst_data["language"],
            "Electude Domain": inst_data["domain"],
            "Registration Date": (
                datetime.now() - timedelta(days=random.randint(30, 1000))
            ).strftime("%Y-%m-%d"),
            "Active Status": random.choice(["Active", "Active", "Active", "Inactive"])
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    
    # Add some missing values for realism
    mask = np.random.random(len(df)) < 0.05
    df.loc[mask, "EMAIL"] = np.nan
    
    mask = np.random.random(len(df)) < 0.08
    df.loc[mask, "Phone number"] = np.nan
    
    return df


def generate_survey_data(main_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate survey/feedback data correlated with main data.
    
    Args:
        main_df: Main dataframe to correlate with
        
    Returns:
        DataFrame with survey data
    """
    records = []
    institutions = main_df["Institution"].unique()
    
    for institution in institutions:
        # 5-20 survey responses per institution
        n_responses = random.randint(5, 20)
        
        for _ in range(n_responses):
            # Generate satisfaction score with some correlation to institution size
            satisfaction = np.clip(
                np.random.normal(3.5, 0.8), 1, 5
            )
            
            record = {
                "Institution": institution,
                "Respondent Type": random.choice(["Teacher", "Student", "Administrator"]),
                "Satisfaction Score": round(satisfaction, 1),
                "Feedback": generate_feedback(satisfaction),
                "Response Date": (
                    datetime.now() - timedelta(days=random.randint(1, 90))
                ).strftime("%Y-%m-%d")
            }
            records.append(record)
    
    return pd.DataFrame(records)


def save_sample_data(output_dir: str = "."):
    """
    Generate and save sample data files.
    
    Args:
        output_dir: Directory to save files
    """
    import os
    
    # Generate main data
    print("Generating main dataset...")
    main_df = generate_main_data(500)
    main_path = os.path.join(output_dir, "electude_data.csv")
    main_df.to_csv(main_path, index=False)
    print(f"Saved main data to {main_path}")
    
    # Generate survey data
    print("Generating survey dataset...")
    survey_df = generate_survey_data(main_df)
    survey_path = os.path.join(output_dir, "survey_data.csv")
    survey_df.to_csv(survey_path, index=False)
    print(f"Saved survey data to {survey_path}")
    
    # Print summary
    print("\n" + "="*50)
    print("SAMPLE DATA GENERATION COMPLETE")
    print("="*50)
    print(f"Main dataset: {len(main_df)} records")
    print(f"Institutions: {main_df['Institution'].nunique()}")
    print(f"Countries: {main_df['Institution'].str.split('-').str[-1].str.strip().nunique()}")
    print(f"Survey responses: {len(survey_df)}")
    print("="*50)


if __name__ == "__main__":
    save_sample_data()