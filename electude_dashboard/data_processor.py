"""
Data Processing Utilities for Electude Africa Analytics Dashboard
Handles data loading, cleaning, transformation, and validation
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
import streamlit as st
from datetime import datetime


@dataclass
class DataQualityReport:
    """Container for data quality metrics."""
    total_records: int
    complete_records: int
    missing_emails: int
    missing_phones: int
    missing_students: int
    duplicate_records: int
    quality_score: float  # 0-100
    
    def to_dict(self) -> Dict:
        return {
            "Total Records": self.total_records,
            "Complete Records": self.complete_records,
            "Missing Emails": self.missing_emails,
            "Missing Phone Numbers": self.missing_phones,
            "Missing Student Count": self.missing_students,
            "Duplicate Records": self.duplicate_records,
            "Quality Score": f"{self.quality_score:.1f}%"
        }


class DataLoader:
    """
    Handles loading and initial processing of data files.
    Implements caching for optimal performance.
    """
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def load_main_data(filepath: str = "electude_data.csv") -> pd.DataFrame:
        """
        Load and perform initial validation on main dataset.
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            DataFrame with loaded data
        """
        try:
            df = pd.read_csv(filepath)
            return df
        except FileNotFoundError:
            st.error(f"Data file not found: {filepath}")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return pd.DataFrame()
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def load_survey_data(filepath: str = "survey_data.csv") -> pd.DataFrame:
        """
        Load survey/feedback data.
        
        Args:
            filepath: Path to the survey CSV file
            
        Returns:
            DataFrame with survey data
        """
        try:
            df = pd.read_csv(filepath)
            return df
        except FileNotFoundError:
            return pd.DataFrame()
        except Exception:
            return pd.DataFrame()


class DataCleaner:
    """
    Handles all data cleaning and preprocessing operations.
    Implements industry best practices for data hygiene.
    """
    
    REQUIRED_COLUMNS = [
        "Institution", "Teacher / Trainer", "Number of Students",
        "EMAIL", "Phone number", "Language", "Electude Domain"
    ]
    
    @classmethod
    def clean_dataframe(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply comprehensive cleaning pipeline to the dataframe.
        
        Args:
            df: Raw input dataframe
            
        Returns:
            Cleaned dataframe ready for analysis
        """
        if df.empty:
            return df
        
        df_clean = df.copy()
        
        # Apply individual cleaning steps
        df_clean = cls._clean_institution_names(df_clean)
        df_clean = cls._clean_numeric_columns(df_clean)
        df_clean = cls._clean_categorical_columns(df_clean)
        df_clean = cls._clean_contact_info(df_clean)
        df_clean = cls._extract_derived_fields(df_clean)
        
        return df_clean
    
    @staticmethod
    def _clean_institution_names(df: pd.DataFrame) -> pd.DataFrame:
        """Standardize institution names and extract country."""
        # Forward fill institution names if there are gaps
        if "Institution" in df.columns:
            df["Institution"] = df["Institution"].fillna(method="ffill")
            # Strip whitespace and standardize
            df["Institution"] = df["Institution"].str.strip()
        
        return df
    
    @staticmethod
    def _clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate numeric columns."""
        if "Number of Students" in df.columns:
            df["Number of Students"] = pd.to_numeric(
                df["Number of Students"], 
                errors="coerce"
            ).fillna(0).astype(int)
        
        return df
    
    @staticmethod
    def _clean_categorical_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Clean categorical columns with forward fill for missing values."""
        categorical_cols = ["Electude Domain", "Language"]
        
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].fillna(method="ffill")
                df[col] = df[col].str.strip() if df[col].dtype == object else df[col]
        
        # Handle teacher/trainer names
        if "Teacher / Trainer" in df.columns:
            df["Teacher / Trainer"] = df["Teacher / Trainer"].fillna("Unknown")
            df["Teacher / Trainer"] = df["Teacher / Trainer"].str.strip()
        
        return df
    
    @staticmethod
    def _clean_contact_info(df: pd.DataFrame) -> pd.DataFrame:
        """Standardize email and phone number formats."""
        if "EMAIL" in df.columns:
            df["EMAIL"] = df["EMAIL"].str.lower().str.strip()
        
        if "Phone number" in df.columns:
            # Basic phone number cleaning
            df["Phone number"] = df["Phone number"].astype(str).str.strip()
        
        return df
    
    @staticmethod
    def _extract_derived_fields(df: pd.DataFrame) -> pd.DataFrame:
        """Extract additional fields from existing data."""
        # Extract country from institution name
        if "Institution" in df.columns:
            df["Country"] = df["Institution"].str.split("-").str[-1].str.strip()
        
        # Extract institution type (if applicable)
        if "Institution" in df.columns:
            df["Institution_Type"] = df["Institution"].apply(
                lambda x: "TVET" if "TVET" in str(x).upper() else 
                         "Technical" if "TECHNICAL" in str(x).upper() else
                         "Institute" if "INSTITUTE" in str(x).upper() else
                         "College" if "COLLEGE" in str(x).upper() else "Other"
            )
        
        return df


class DataValidator:
    """
    Validates data quality and generates reports.
    Implements comprehensive validation rules.
    """
    
    @staticmethod
    def generate_quality_report(df: pd.DataFrame) -> DataQualityReport:
        """
        Generate a comprehensive data quality report.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            DataQualityReport with metrics
        """
        if df.empty:
            return DataQualityReport(0, 0, 0, 0, 0, 0, 0.0)
        
        total_records = len(df)
        
        # Count missing values
        missing_emails = df["EMAIL"].isna().sum() if "EMAIL" in df.columns else 0
        missing_phones = df["Phone number"].isna().sum() if "Phone number" in df.columns else 0
        missing_students = (df["Number of Students"] == 0).sum() if "Number of Students" in df.columns else 0
        
        # Check for duplicates
        duplicate_records = df.duplicated().sum()
        
        # Count complete records
        required_cols = ["Institution", "Teacher / Trainer", "EMAIL"]
        complete_mask = df[required_cols].notna().all(axis=1)
        complete_records = complete_mask.sum()
        
        # Calculate quality score
        # Weights: completeness (40%), contacts (30%), no duplicates (30%)
        completeness_score = (complete_records / total_records) * 40
        contact_score = ((total_records - missing_emails - missing_phones) / (total_records * 2)) * 30
        duplicate_score = ((total_records - duplicate_records) / total_records) * 30
        
        quality_score = min(100, max(0, completeness_score + contact_score + duplicate_score))
        
        return DataQualityReport(
            total_records=total_records,
            complete_records=complete_records,
            missing_emails=int(missing_emails),
            missing_phones=int(missing_phones),
            missing_students=int(missing_students),
            duplicate_records=int(duplicate_records),
            quality_score=quality_score
        )


class DataAggregator:
    """
    Handles data aggregation and transformation for visualizations.
    Provides methods for common aggregation patterns.
    """
    
    @staticmethod
    def aggregate_by_institution(df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate student and teacher counts by institution.
        
        Args:
            df: Input dataframe
            
        Returns:
            Aggregated dataframe with institution-level metrics
        """
        if df.empty:
            return pd.DataFrame()
        
        agg_df = df.groupby("Institution").agg({
            "Number of Students": "sum",
            "Teacher / Trainer": "count",
            "Country": "first",
            "Language": "first"
        }).reset_index()
        
        agg_df.columns = [
            "Institution", "Total Students", 
            "Total Teachers", "Country", "Language"
        ]
        
        return agg_df.sort_values("Total Students", ascending=False)
    
    @staticmethod
    def get_language_distribution(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate language distribution across the dataset.
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with language counts and percentages
        """
        if df.empty or "Language" not in df.columns:
            return pd.DataFrame()
        
        lang_dist = df.groupby("Language").agg({
            "Number of Students": "sum"
        }).reset_index()
        
        lang_dist["Percentage"] = (
            lang_dist["Number of Students"] / lang_dist["Number of Students"].sum() * 100
        ).round(1)
        
        lang_dist = lang_dist.sort_values("Number of Students", ascending=False)
        lang_dist.columns = ["Language", "Students", "Percentage"]
        
        return lang_dist
    
    @staticmethod
    def get_country_distribution(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate distribution by country.
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with country-level metrics
        """
        if df.empty or "Country" not in df.columns:
            return pd.DataFrame()
        
        country_dist = df.groupby("Country").agg({
            "Number of Students": "sum",
            "Institution": "nunique",
            "Teacher / Trainer": "count"
        }).reset_index()
        
        country_dist.columns = ["Country", "Students", "Institutions", "Teachers"]
        country_dist = country_dist.sort_values("Students", ascending=False)
        
        return country_dist
    
    @staticmethod
    def get_top_institutions(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        """
        Get top N institutions by student count.
        
        Args:
            df: Input dataframe
            n: Number of top institutions to return
            
        Returns:
            DataFrame with top institutions
        """
        agg_df = DataAggregator.aggregate_by_institution(df)
        return agg_df.head(n)


def process_pipeline(df: pd.DataFrame) -> Tuple[pd.DataFrame, DataQualityReport]:
    """
    Execute the complete data processing pipeline.
    
    Args:
        df: Raw input dataframe
        
    Returns:
        Tuple of (cleaned dataframe, quality report)
    """
    # Clean the data
    df_clean = DataCleaner.clean_dataframe(df)
    
    # Generate quality report
    quality_report = DataValidator.generate_quality_report(df_clean)
    
    return df_clean, quality_report