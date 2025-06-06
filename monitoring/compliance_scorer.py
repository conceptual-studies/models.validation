#!/usr/bin/env python3
"""
FCM Repository Compliance Scoring System
Implementation of Layer 4 health monitoring from the GitHub Repository Model
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class HealthCategory(Enum):
    """Health metric categories"""
    STRUCTURAL = "structural"
    CONTENT = "content" 
    PROCESS = "process"
    SECURITY = "security"
    EVOLUTION = "evolution"


@dataclass
class HealthMetric:
    """Individual health metric"""
    name: str
    category: HealthCategory
    value: float
    weight: float
    status: str = "unknown"  # excellent, good, fair, poor, critical
    trend: str = "stable"    # improving, stable, declining
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class ComplianceScore:
    """Complete compliance scoring result"""
    overall_score: float
    category_scores: Dict[str, float] = field(default_factory=dict)
    metrics: List[HealthMetric] = field(default_factory=list)
    compliance_level: str = "basic"
    health_grade: str = "C"
    trend_analysis: Dict[str, str] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


class ComplianceScorer:
    """
    Advanced compliance scoring implementing Layer 4 dynamics from the formal model
    """
    
    def __init__(self):
        """Initialize scorer with metric definitions"""
        self.metric_definitions = self._load_metric_definitions()
        self.scoring_algorithms = self._load_scoring_algorithms()
        self.history_path = Path("compliance_history.json")
    
    def _load_metric_definitions(self) -> Dict[str, Dict]:
        """Define all health metrics from the formal model"""
        return {
            "structural_health": {
                "category": HealthCategory.STRUCTURAL,
                "weight": 0.25,
                "components": {
                    "directory_compliance": 0.4,
                    "file_presence": 0.3,
                    "naming_conventions": 0.2,
                    "organization_clarity": 0.1
                },
                "thresholds": {
                    "excellent": 0.95,
                    "good": 0.85,
                    "fair": 0.70,
                    "poor": 0.50,
                    "critical": 0.30
                }
            },
            
            "content_health": {
                "category": HealthCategory.CONTENT,
                "weight": 0.25,
                "components": {
                    "documentation_completeness": 0.35,
                    "fcm_model_compliance": 0.30,
                    "manifest_validity": 0.20,
                    "content_quality": 0.15
                },
                "thresholds": {
                    "excellent": 0.90,
                    "good": 0.80,
                    "fair": 0.65,
                    "poor": 0.45,
                    "critical": 0.25
                }
            },
            
            "process_health": {
                "category": HealthCategory.PROCESS,
                "weight": 0.20,
                "components": {
                    "automation_presence": 0.4,
                    "validation_integration": 0.3,
                    "ci_cd_effectiveness": 0.2,
                    "workflow_optimization": 0.1
                },
                "thresholds": {
                    "excellent": 0.85,
                    "good": 0.70,
                    "fair": 0.55,
                    "poor": 0.35,
                    "critical": 0.20
                }
            },
            
            "security_health": {
                "category": HealthCategory.SECURITY,
                "weight": 0.15,
                "components": {
                    "security_policy": 0.4,
                    "dependency_scanning": 0.3,
                    "access_control": 0.2,
                    "vulnerability_management": 0.1
                },
                "thresholds": {
                    "excellent": 0.90,
                    "good": 0.75,
                    "fair": 0.60,
                    "poor": 0.40,
                    "critical": 0.20
                }
            },
            
            "evolution_health": {
                "category": HealthCategory.EVOLUTION,
                "weight": 0.15,
                "components": {
                    "change_frequency": 0.3,
                    "improvement_trend": 0.3,
                    "adaptation_capability": 0.2,
                    "innovation_indicators": 0.2
                },
                "thresholds": {
                    "excellent": 0.80,
                    "good": 0.65,
                    "fair": 0.50,
                    "poor": 0.35,
                    "critical": 0.20
                }
            }
        }
    
    def _load_scoring_algorithms(self) -> Dict[str, callable]:
        """Define scoring algorithms for different aspects"""
        return {
            "weighted_average": self._weighted_average_score,
            "exponential_decay": self._exponential_decay_score,
            "trend_adjusted": self._trend_adjusted_score,
            "penalty_based": self._penalty_based_score
        }
    
    def calculate_compliance_score(self, validation_result: Dict[str, Any], 
                                 historical_data: List[Dict] = None) -> ComplianceScore:
        """
        Main scoring function implementing Layer 4 scoring dynamics
        """
        # Initialize with placeholder score, will be calculated below
        score = ComplianceScore(overall_score=0.0)
        
        # Extract base metrics from validation result
        base_metrics = self._extract_base_metrics(validation_result)
        
        # Calculate category scores
        for category_name, definition in self.metric_definitions.items():
            category_score = self._calculate_category_score(
                category_name, base_metrics, definition
            )
            score.category_scores[category_name] = category_score
            
            # Create health metric
            metric = HealthMetric(
                name=category_name,
                category=definition["category"],
                value=category_score,
                weight=definition["weight"],
                status=self._determine_status(category_score, definition["thresholds"])
            )
            score.metrics.append(metric)
        
        # Calculate overall score using weighted average
        score.overall_score = sum(
            score.category_scores[name] * definition["weight"]
            for name, definition in self.metric_definitions.items()
        )
        
        # Determine compliance level
        score.compliance_level = self._determine_compliance_level(score.overall_score)
        
        # Calculate health grade
        score.health_grade = self._calculate_health_grade(score.overall_score)
        
        # Analyze trends if historical data available
        if historical_data:
            score.trend_analysis = self._analyze_trends(historical_data, score)
            self._adjust_score_for_trends(score)
        
        # Generate recommendations
        score.recommendations = self._generate_recommendations(score)
        
        # Save to history
        self._save_to_history(score)
        
        return score
    
    def _extract_base_metrics(self, validation_result: Dict[str, Any]) -> Dict[str, float]:
        """Extract base metrics from validation result"""
        health_metrics = validation_result.get("health_metrics", {})
        
        return {
            "structural_health": health_metrics.get("structural_health", 0.0),
            "content_health": health_metrics.get("content_health", 0.0),
            "process_health": health_metrics.get("process_health", 0.0),
            "security_health": health_metrics.get("security_health", 0.0),
            "overall_health": health_metrics.get("overall_health", 0.0)
        }
    
    def _calculate_category_score(self, category_name: str, base_metrics: Dict[str, float],
                                definition: Dict[str, Any]) -> float:
        """Calculate score for a specific category"""
        if category_name in base_metrics:
            base_score = base_metrics[category_name]
        else:
            # Calculate from components if base not available
            base_score = 0.5  # Default neutral score
        
        # Apply category-specific adjustments
        if category_name == "evolution_health":
            # Evolution health needs special calculation
            return self._calculate_evolution_health(base_metrics)
        
        return base_score
    
    def _calculate_evolution_health(self, base_metrics: Dict[str, float]) -> float:
        """Calculate evolution health based on improvement patterns"""
        # This would analyze commit history, improvement trends, etc.
        # For now, return a calculated estimate
        avg_health = sum(base_metrics.values()) / len(base_metrics) if base_metrics else 0.5
        
        # Evolution health correlates with overall health but with some randomness
        # representing adaptation and change capability
        evolution_factor = 0.8 + (avg_health * 0.2)  # Base evolution capability
        return min(1.0, evolution_factor)
    
    def _determine_status(self, score: float, thresholds: Dict[str, float]) -> str:
        """Determine status level based on score and thresholds"""
        if score >= thresholds["excellent"]:
            return "excellent"
        elif score >= thresholds["good"]:
            return "good"
        elif score >= thresholds["fair"]:
            return "fair"
        elif score >= thresholds["poor"]:
            return "poor"
        else:
            return "critical"
    
    def _determine_compliance_level(self, overall_score: float) -> str:
        """Map overall score to compliance level"""
        if overall_score >= 0.90:
            return "exemplary"
        elif overall_score >= 0.75:
            return "secure"
        elif overall_score >= 0.60:
            return "tested"
        elif overall_score >= 0.45:
            return "documented"
        elif overall_score >= 0.30:
            return "structured"
        else:
            return "basic"
    
    def _calculate_health_grade(self, overall_score: float) -> str:
        """Calculate letter grade for health"""
        if overall_score >= 0.95:
            return "A+"
        elif overall_score >= 0.90:
            return "A"
        elif overall_score >= 0.85:
            return "A-"
        elif overall_score >= 0.80:
            return "B+"
        elif overall_score >= 0.75:
            return "B"
        elif overall_score >= 0.70:
            return "B-"
        elif overall_score >= 0.65:
            return "C+"
        elif overall_score >= 0.60:
            return "C"
        elif overall_score >= 0.55:
            return "C-"
        elif overall_score >= 0.50:
            return "D+"
        elif overall_score >= 0.45:
            return "D"
        else:
            return "F"
    
    def _analyze_trends(self, historical_data: List[Dict], current_score: ComplianceScore) -> Dict[str, str]:
        """Analyze trends from historical data"""
        if len(historical_data) < 2:
            return {"overall": "insufficient_data"}
        
        trends = {}
        
        # Analyze overall trend
        recent_scores = [entry["overall_score"] for entry in historical_data[-5:]]
        if len(recent_scores) >= 2:
            if recent_scores[-1] > recent_scores[0] * 1.05:
                trends["overall"] = "improving"
            elif recent_scores[-1] < recent_scores[0] * 0.95:
                trends["overall"] = "declining"
            else:
                trends["overall"] = "stable"
        
        # Analyze category trends
        for category in self.metric_definitions.keys():
            category_scores = [
                entry.get("category_scores", {}).get(category, 0.5)
                for entry in historical_data[-3:]
            ]
            if len(category_scores) >= 2:
                if category_scores[-1] > category_scores[0]:
                    trends[category] = "improving"
                elif category_scores[-1] < category_scores[0]:
                    trends[category] = "declining"
                else:
                    trends[category] = "stable"
        
        return trends
    
    def _adjust_score_for_trends(self, score: ComplianceScore):
        """Adjust score based on trend analysis"""
        trend = score.trend_analysis.get("overall", "stable")
        
        if trend == "improving":
            # Boost score slightly for positive trends
            score.overall_score = min(1.0, score.overall_score * 1.02)
        elif trend == "declining":
            # Penalize slightly for negative trends
            score.overall_score = max(0.0, score.overall_score * 0.98)
        
        # Update metrics trends
        for metric in score.metrics:
            category_trend = score.trend_analysis.get(metric.name, "stable")
            metric.trend = category_trend
    
    def _generate_recommendations(self, score: ComplianceScore) -> List[str]:
        """Generate actionable recommendations based on score analysis"""
        recommendations = []
        
        # Category-specific recommendations
        for metric in score.metrics:
            if metric.status == "critical":
                recommendations.append(
                    f"🚨 CRITICAL: {metric.name.replace('_', ' ').title()} needs immediate attention (score: {metric.value:.2f})"
                )
            elif metric.status == "poor":
                recommendations.append(
                    f"⚠️ {metric.name.replace('_', ' ').title()} below acceptable threshold (score: {metric.value:.2f})"
                )
            elif metric.trend == "declining":
                recommendations.append(
                    f"📉 {metric.name.replace('_', ' ').title()} is declining - investigate causes"
                )
        
        # Overall recommendations
        if score.overall_score < 0.5:
            recommendations.append("🔧 Consider running automated remediation tools")
            recommendations.append("📚 Review FCM repository best practices documentation")
        
        if score.health_grade in ["D", "F"]:
            recommendations.append("🏥 Repository health is poor - schedule comprehensive review")
        
        # Positive reinforcement
        if score.overall_score > 0.85:
            recommendations.append("✨ Excellent repository health - consider sharing as example")
        
        return recommendations
    
    def _save_to_history(self, score: ComplianceScore):
        """Save score to historical tracking"""
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "overall_score": score.overall_score,
            "compliance_level": score.compliance_level,
            "health_grade": score.health_grade,
            "category_scores": score.category_scores,
            "trend_analysis": score.trend_analysis
        }
        
        # Load existing history
        history = []
        if self.history_path.exists():
            try:
                with open(self.history_path, 'r') as f:
                    history = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                history = []
        
        # Add new entry
        history.append(history_entry)
        
        # Keep only last 100 entries
        history = history[-100:]
        
        # Save updated history
        with open(self.history_path, 'w') as f:
            json.dump(history, f, indent=2)
    
    def _weighted_average_score(self, scores: List[float], weights: List[float]) -> float:
        """Calculate weighted average score"""
        if not scores or not weights or len(scores) != len(weights):
            return 0.0
        return sum(s * w for s, w in zip(scores, weights)) / sum(weights)
    
    def _exponential_decay_score(self, scores: List[float], decay_factor: float = 0.9) -> float:
        """Calculate score with exponential decay for older entries"""
        if not scores:
            return 0.0
        
        weighted_sum = 0.0
        weight_sum = 0.0
        
        for i, score in enumerate(reversed(scores)):
            weight = decay_factor ** i
            weighted_sum += score * weight
            weight_sum += weight
        
        return weighted_sum / weight_sum if weight_sum > 0 else 0.0
    
    def _trend_adjusted_score(self, scores: List[float], trend_weight: float = 0.1) -> float:
        """Adjust score based on trend direction"""
        if len(scores) < 2:
            return scores[0] if scores else 0.0
        
        base_score = scores[-1]
        trend = (scores[-1] - scores[0]) / len(scores)
        
        return base_score + (trend * trend_weight)
    
    def _penalty_based_score(self, base_score: float, violations: List[str]) -> float:
        """Apply penalties based on violation severity"""
        penalty = 0.0
        
        for violation in violations:
            if "critical" in violation.lower() or "missing required" in violation.lower():
                penalty += 0.1
            elif "warning" in violation.lower() or "recommended" in violation.lower():
                penalty += 0.02
            else:
                penalty += 0.05
        
        return max(0.0, base_score - penalty)
    
    def generate_report(self, score: ComplianceScore) -> str:
        """Generate human-readable compliance report"""
        report = []
        report.append("# FCM Repository Compliance Report")
        report.append("=" * 40)
        report.append("")
        report.append(f"**Overall Score:** {score.overall_score:.2f} ({score.health_grade})")
        report.append(f"**Compliance Level:** {score.compliance_level.upper()}")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Category breakdown
        report.append("## Category Scores")
        report.append("")
        for metric in score.metrics:
            status_emoji = {
                "excellent": "🟢",
                "good": "🔵", 
                "fair": "🟡",
                "poor": "🟠",
                "critical": "🔴"
            }.get(metric.status, "⚪")
            
            trend_emoji = {
                "improving": "📈",
                "stable": "➡️",
                "declining": "📉"
            }.get(metric.trend, "➡️")
            
            report.append(f"- **{metric.name.replace('_', ' ').title()}:** {metric.value:.2f} {status_emoji} {trend_emoji}")
        
        report.append("")
        
        # Recommendations
        if score.recommendations:
            report.append("## Recommendations")
            report.append("")
            for rec in score.recommendations:
                report.append(f"- {rec}")
            report.append("")
        
        # Trend analysis
        if score.trend_analysis:
            report.append("## Trend Analysis")
            report.append("")
            for category, trend in score.trend_analysis.items():
                report.append(f"- **{category.replace('_', ' ').title()}:** {trend}")
        
        return "\n".join(report)


def main():
    """CLI interface for compliance scoring"""
    import argparse
    
    parser = argparse.ArgumentParser(description="FCM Repository Compliance Scorer")
    parser.add_argument("validation_result", help="Path to validation result JSON file")
    parser.add_argument("--history", help="Path to historical data JSON file")
    parser.add_argument("--format", choices=["json", "text", "markdown"], default="text")
    
    args = parser.parse_args()
    
    # Load validation result
    with open(args.validation_result, 'r') as f:
        validation_result = json.load(f)
    
    # Load historical data if provided
    historical_data = []
    if args.history and Path(args.history).exists():
        with open(args.history, 'r') as f:
            historical_data = json.load(f)
    
    # Calculate compliance score
    scorer = ComplianceScorer()
    score = scorer.calculate_compliance_score(validation_result, historical_data)
    
    # Output results
    if args.format == "json":
        output = {
            "overall_score": score.overall_score,
            "compliance_level": score.compliance_level,
            "health_grade": score.health_grade,
            "category_scores": score.category_scores,
            "recommendations": score.recommendations,
            "trend_analysis": score.trend_analysis
        }
        print(json.dumps(output, indent=2))
    elif args.format == "markdown":
        print(scorer.generate_report(score))
    else:
        print(scorer.generate_report(score))


if __name__ == "__main__":
    main()