#!/usr/bin/env python3
"""
FCM Repository Health Monitoring Dashboard
Implementation of Layer 5 organizational intelligence from the GitHub Repository Model
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import argparse


@dataclass
class RepositoryHealth:
    """Repository health snapshot"""
    repo_name: str
    timestamp: datetime
    overall_score: float
    compliance_level: str
    health_grade: str
    category_scores: Dict[str, float]
    violations_count: int
    trend: str
    last_updated: datetime


class HealthDatabase:
    """SQLite database for health tracking"""
    
    def __init__(self, db_path: str = "health_monitoring.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS repository_health (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    overall_score REAL NOT NULL,
                    compliance_level TEXT NOT NULL,
                    health_grade TEXT NOT NULL,
                    structural_health REAL,
                    content_health REAL,
                    process_health REAL,
                    security_health REAL,
                    evolution_health REAL,
                    violations_count INTEGER,
                    trend TEXT,
                    raw_data TEXT
                );
                
                CREATE TABLE IF NOT EXISTS validation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    violation_type TEXT NOT NULL,
                    violation_message TEXT NOT NULL,
                    severity TEXT NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS remediation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    action_description TEXT NOT NULL,
                    safety_level TEXT NOT NULL,
                    success BOOLEAN NOT NULL
                );
                
                CREATE INDEX IF NOT EXISTS idx_repo_timestamp ON repository_health(repo_name, timestamp);
                CREATE INDEX IF NOT EXISTS idx_violation_repo ON validation_history(repo_name, timestamp);
                CREATE INDEX IF NOT EXISTS idx_remediation_repo ON remediation_history(repo_name, timestamp);
            """)
    
    def store_health_snapshot(self, health: RepositoryHealth, raw_data: Dict[str, Any]):
        """Store health snapshot in database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO repository_health (
                    repo_name, timestamp, overall_score, compliance_level, health_grade,
                    structural_health, content_health, process_health, security_health, evolution_health,
                    violations_count, trend, raw_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                health.repo_name,
                health.timestamp.isoformat(),
                health.overall_score,
                health.compliance_level,
                health.health_grade,
                health.category_scores.get("structural_health", 0.0),
                health.category_scores.get("content_health", 0.0),
                health.category_scores.get("process_health", 0.0),
                health.category_scores.get("security_health", 0.0),
                health.category_scores.get("evolution_health", 0.0),
                health.violations_count,
                health.trend,
                json.dumps(raw_data)
            ))
    
    def get_repository_history(self, repo_name: str, days: int = 30) -> List[RepositoryHealth]:
        """Get repository health history"""
        cutoff = datetime.now() - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT repo_name, timestamp, overall_score, compliance_level, health_grade,
                       structural_health, content_health, process_health, security_health, evolution_health,
                       violations_count, trend
                FROM repository_health
                WHERE repo_name = ? AND timestamp > ?
                ORDER BY timestamp DESC
            """, (repo_name, cutoff.isoformat()))
            
            results = []
            for row in cursor.fetchall():
                category_scores = {
                    "structural_health": row[5],
                    "content_health": row[6],
                    "process_health": row[7],
                    "security_health": row[8],
                    "evolution_health": row[9]
                }
                
                health = RepositoryHealth(
                    repo_name=row[0],
                    timestamp=datetime.fromisoformat(row[1]),
                    overall_score=row[2],
                    compliance_level=row[3],
                    health_grade=row[4],
                    category_scores=category_scores,
                    violations_count=row[10],
                    trend=row[11],
                    last_updated=datetime.fromisoformat(row[1])
                )
                results.append(health)
            
            return results
    
    def get_all_repositories(self) -> List[str]:
        """Get list of all monitored repositories"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT DISTINCT repo_name FROM repository_health")
            return [row[0] for row in cursor.fetchall()]


class HealthDashboard:
    """
    Health monitoring dashboard implementing Layer 5 organizational intelligence
    """
    
    def __init__(self, db_path: str = "health_monitoring.db"):
        self.db = HealthDatabase(db_path)
    
    def update_repository_health(self, repo_name: str, validation_result: Dict[str, Any]):
        """Update health data for a repository"""
        # Extract health metrics
        health = RepositoryHealth(
            repo_name=repo_name,
            timestamp=datetime.now(),
            overall_score=validation_result.get("score", 0.0),
            compliance_level=validation_result.get("compliance_level", "basic"),
            health_grade=validation_result.get("health_grade", "F"),
            category_scores=validation_result.get("health_metrics", {}),
            violations_count=len(validation_result.get("violations", [])),
            trend=validation_result.get("trend", "stable"),
            last_updated=datetime.now()
        )
        
        # Store in database
        self.db.store_health_snapshot(health, validation_result)
        
        return health
    
    def generate_dashboard_report(self, format_type: str = "markdown") -> str:
        """Generate comprehensive dashboard report"""
        repositories = self.db.get_all_repositories()
        
        if format_type == "markdown":
            return self._generate_markdown_dashboard(repositories)
        elif format_type == "html":
            return self._generate_html_dashboard(repositories)
        else:
            return self._generate_text_dashboard(repositories)
    
    def _generate_markdown_dashboard(self, repositories: List[str]) -> str:
        """Generate markdown dashboard"""
        report = []
        report.append("# FCM Repository Health Dashboard")
        report.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        report.append("")
        
        # Overall summary
        summary = self._calculate_summary_stats(repositories)
        report.append("## 📊 Organization Summary")
        report.append("")
        report.append(f"- **Total Repositories:** {summary['total_repos']}")
        report.append(f"- **Average Health Score:** {summary['avg_score']:.2f}")
        report.append(f"- **Healthy Repositories:** {summary['healthy_count']}/{summary['total_repos']}")
        report.append(f"- **Critical Issues:** {summary['critical_count']}")
        report.append("")
        
        # Health distribution
        report.append("## 🎯 Compliance Distribution")
        report.append("")
        report.append("| Level | Count | Percentage |")
        report.append("|-------|-------|------------|")
        for level, count in summary['compliance_distribution'].items():
            percentage = (count / summary['total_repos'] * 100) if summary['total_repos'] > 0 else 0
            report.append(f"| {level.title()} | {count} | {percentage:.1f}% |")
        report.append("")
        
        # Repository details
        report.append("## 📁 Repository Details")
        report.append("")
        report.append("| Repository | Score | Grade | Level | Trend | Issues |")
        report.append("|------------|-------|-------|-------|-------|--------|")
        
        for repo_name in repositories:
            latest = self._get_latest_health(repo_name)
            if latest:
                trend_emoji = {"improving": "📈", "stable": "➡️", "declining": "📉"}.get(latest.trend, "➡️")
                report.append(f"| {repo_name} | {latest.overall_score:.2f} | {latest.health_grade} | {latest.compliance_level} | {trend_emoji} | {latest.violations_count} |")
        
        report.append("")
        
        # Critical issues
        critical_repos = [repo for repo in repositories if self._get_latest_health(repo) and self._get_latest_health(repo).overall_score < 0.4]
        if critical_repos:
            report.append("## 🚨 Critical Issues")
            report.append("")
            for repo_name in critical_repos:
                latest = self._get_latest_health(repo_name)
                report.append(f"- **{repo_name}**: Score {latest.overall_score:.2f} - {latest.violations_count} violations")
            report.append("")
        
        # Trends analysis
        report.append("## 📈 Trend Analysis")
        report.append("")
        trend_summary = self._analyze_trends(repositories)
        for trend_type, repos in trend_summary.items():
            if repos:
                emoji = {"improving": "📈", "stable": "➡️", "declining": "📉"}.get(trend_type, "➡️")
                report.append(f"### {emoji} {trend_type.title()} ({len(repos)} repositories)")
                for repo in repos:
                    report.append(f"- {repo}")
                report.append("")
        
        # Recommendations
        recommendations = self._generate_organizational_recommendations(repositories)
        if recommendations:
            report.append("## 💡 Organizational Recommendations")
            report.append("")
            for rec in recommendations:
                report.append(f"- {rec}")
            report.append("")
        
        return "\n".join(report)
    
    def _generate_html_dashboard(self, repositories: List[str]) -> str:
        """Generate HTML dashboard with charts"""
        # Basic HTML dashboard - could be enhanced with proper charting
        summary = self._calculate_summary_stats(repositories)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>FCM Repository Health Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #f5f5f5; border-radius: 5px; }}
                .critical {{ background: #ffebee; border-left: 4px solid #f44336; }}
                .good {{ background: #e8f5e8; border-left: 4px solid #4caf50; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>FCM Repository Health Dashboard</h1>
            <p><em>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
            
            <h2>Organization Summary</h2>
            <div class="metric">
                <strong>Total Repositories</strong><br>
                {summary['total_repos']}
            </div>
            <div class="metric">
                <strong>Average Health Score</strong><br>
                {summary['avg_score']:.2f}
            </div>
            <div class="metric">
                <strong>Healthy Repositories</strong><br>
                {summary['healthy_count']}/{summary['total_repos']}
            </div>
            <div class="metric">
                <strong>Critical Issues</strong><br>
                {summary['critical_count']}
            </div>
            
            <h2>Repository Status</h2>
            <table>
                <tr>
                    <th>Repository</th>
                    <th>Score</th>
                    <th>Grade</th>
                    <th>Compliance Level</th>
                    <th>Trend</th>
                    <th>Issues</th>
                </tr>
        """
        
        for repo_name in repositories:
            latest = self._get_latest_health(repo_name)
            if latest:
                row_class = "critical" if latest.overall_score < 0.4 else "good" if latest.overall_score > 0.8 else ""
                html += f"""
                <tr class="{row_class}">
                    <td>{repo_name}</td>
                    <td>{latest.overall_score:.2f}</td>
                    <td>{latest.health_grade}</td>
                    <td>{latest.compliance_level}</td>
                    <td>{latest.trend}</td>
                    <td>{latest.violations_count}</td>
                </tr>
                """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        return html
    
    def _get_latest_health(self, repo_name: str) -> Optional[RepositoryHealth]:
        """Get latest health snapshot for repository"""
        history = self.db.get_repository_history(repo_name, days=1)
        return history[0] if history else None
    
    def _calculate_summary_stats(self, repositories: List[str]) -> Dict[str, Any]:
        """Calculate organization-wide summary statistics"""
        total_repos = len(repositories)
        scores = []
        compliance_levels = {"basic": 0, "structured": 0, "documented": 0, "tested": 0, "secure": 0, "exemplary": 0}
        critical_count = 0
        healthy_count = 0
        
        for repo_name in repositories:
            latest = self._get_latest_health(repo_name)
            if latest:
                scores.append(latest.overall_score)
                compliance_levels[latest.compliance_level] = compliance_levels.get(latest.compliance_level, 0) + 1
                
                if latest.overall_score < 0.4:
                    critical_count += 1
                elif latest.overall_score > 0.7:
                    healthy_count += 1
        
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        return {
            "total_repos": total_repos,
            "avg_score": avg_score,
            "healthy_count": healthy_count,
            "critical_count": critical_count,
            "compliance_distribution": compliance_levels
        }
    
    def _analyze_trends(self, repositories: List[str]) -> Dict[str, List[str]]:
        """Analyze trends across repositories"""
        trends = {"improving": [], "stable": [], "declining": []}
        
        for repo_name in repositories:
            latest = self._get_latest_health(repo_name)
            if latest:
                trends[latest.trend].append(repo_name)
        
        return trends
    
    def _generate_organizational_recommendations(self, repositories: List[str]) -> List[str]:
        """Generate organization-level recommendations"""
        recommendations = []
        summary = self._calculate_summary_stats(repositories)
        
        # Critical issues
        if summary["critical_count"] > 0:
            recommendations.append(f"🚨 {summary['critical_count']} repositories have critical issues requiring immediate attention")
        
        # Low average score
        if summary["avg_score"] < 0.6:
            recommendations.append("📈 Organization-wide health score is below target (0.6) - consider training or process improvements")
        
        # Compliance distribution
        basic_percentage = (summary["compliance_distribution"]["basic"] / summary["total_repos"]) * 100
        if basic_percentage > 30:
            recommendations.append(f"📋 {basic_percentage:.1f}% of repositories at basic compliance - implement organization-wide standards")
        
        # Success patterns
        if summary["healthy_count"] > summary["total_repos"] * 0.7:
            recommendations.append("✅ Strong overall repository health - document and share best practices")
        
        return recommendations
    
    def generate_repository_report(self, repo_name: str, days: int = 30) -> str:
        """Generate detailed report for specific repository"""
        history = self.db.get_repository_history(repo_name, days)
        
        if not history:
            return f"No health data found for repository: {repo_name}"
        
        latest = history[0]
        
        report = []
        report.append(f"# Repository Health Report: {repo_name}")
        report.append(f"*Period: Last {days} days*")
        report.append("")
        
        # Current status
        report.append("## Current Status")
        report.append(f"- **Overall Score:** {latest.overall_score:.2f} ({latest.health_grade})")
        report.append(f"- **Compliance Level:** {latest.compliance_level}")
        report.append(f"- **Violations:** {latest.violations_count}")
        report.append(f"- **Trend:** {latest.trend}")
        report.append(f"- **Last Updated:** {latest.last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Category breakdown
        report.append("## Category Scores")
        for category, score in latest.category_scores.items():
            report.append(f"- **{category.replace('_', ' ').title()}:** {score:.2f}")
        report.append("")
        
        # Historical trend
        if len(history) > 1:
            report.append("## Historical Trend")
            report.append("```")
            report.append("Date       | Score | Grade | Issues")
            report.append("-----------|-------|-------|-------")
            for h in history[-10:]:  # Last 10 entries
                report.append(f"{h.timestamp.strftime('%Y-%m-%d')} | {h.overall_score:.2f}  | {h.health_grade:5} | {h.violations_count:6}")
            report.append("```")
            report.append("")
        
        return "\n".join(report)


def main():
    """CLI interface for health dashboard"""
    parser = argparse.ArgumentParser(description="FCM Repository Health Dashboard")
    parser.add_argument("--action", choices=["update", "dashboard", "repository"], required=True)
    parser.add_argument("--repo-name", help="Repository name for update/repository actions")
    parser.add_argument("--validation-result", help="Path to validation result JSON")
    parser.add_argument("--format", choices=["markdown", "html", "text"], default="markdown")
    parser.add_argument("--days", type=int, default=30, help="Number of days for historical data")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    dashboard = HealthDashboard()
    
    if args.action == "update":
        if not args.repo_name or not args.validation_result:
            print("Error: --repo-name and --validation-result required for update action")
            return
        
        with open(args.validation_result, 'r') as f:
            validation_result = json.load(f)
        
        health = dashboard.update_repository_health(args.repo_name, validation_result)
        print(f"Updated health data for {args.repo_name}: {health.overall_score:.2f} ({health.health_grade})")
    
    elif args.action == "dashboard":
        report = dashboard.generate_dashboard_report(args.format)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Dashboard report saved to: {args.output}")
        else:
            print(report)
    
    elif args.action == "repository":
        if not args.repo_name:
            print("Error: --repo-name required for repository action")
            return
        
        report = dashboard.generate_repository_report(args.repo_name, args.days)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Repository report saved to: {args.output}")
        else:
            print(report)


if __name__ == "__main__":
    main()