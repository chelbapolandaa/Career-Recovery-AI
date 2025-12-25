from typing import List, Dict, Any
from datetime import datetime
from app.services.groq_service_improved import get_enhanced_groq_coach
import json
import re
from collections import Counter

class StrategyEngine:
    
    def __init__(self):
        self.ai_coach = get_enhanced_groq_coach()
    
    def generate_strategies_based_on_analysis(self, application, all_applications: List) -> Dict[str, Any]:
        print(f"🤖 Generating AI strategies for: {application.job_title} at {application.company}")
        
        try:
            # 1. Prepare data untuk AI analysis
            analysis_data = self._prepare_analysis_data(application, all_applications)
            
            # 2. Get AI analysis - GUNAKAN METHOD YANG BENAR
            ai_insights = self.ai_coach.analyze_career_patterns(analysis_data)  # ← PERBAIKAN DI SINI
            
            # 3. Convert AI insights ke strategies format
            strategies_data = self._convert_insights_to_strategies(ai_insights, application)
            
            # 4. Enhance dengan pattern-based strategies
            enhanced_data = self._enhance_with_pattern_analysis(strategies_data, analysis_data)
            
            return enhanced_data
            
        except Exception as e:
            print(f"❌ AI analysis failed: {e}")
            import traceback
            traceback.print_exc()
            # Fallback ke pattern-based strategies
            return self._generate_pattern_based_strategies(application, all_applications)
    
    def _prepare_analysis_data(self, application, all_applications: List) -> Dict:
        """Prepare comprehensive data untuk GroqCareerCoach"""
        
        # Analyze rejection patterns
        rejection_stats = self._analyze_rejection_patterns(all_applications)
        
        # Prepare role analysis
        role_analysis = self._analyze_role_performance(all_applications)
        
        # Detect patterns
        patterns = self._detect_rejection_patterns(all_applications)
        
        # Analyze timing patterns
        timing_analysis = self._analyze_timing_patterns(all_applications)
        
        # Company analysis
        company_analysis = self._analyze_company_patterns(all_applications)
        
        return {
            'summary': rejection_stats,
            'role_analysis': role_analysis,
            'patterns': patterns,
            'timing_analysis': timing_analysis,
            'company_analysis': company_analysis,
            'current_application': {
                'job_title': application.job_title,
                'company': application.company,
                'role_category': application.role_category,
                'status': application.status,
                'date_applied': application.date_applied.isoformat() if hasattr(application.date_applied, 'isoformat') else str(application.date_applied),
                'notes': application.notes or ""
            },
            'time_period_days': 30  # Default analysis period
        }
    
    def _analyze_rejection_patterns(self, applications: List) -> Dict:
        """Analisis mendalam pola penolakan"""
        
        if not applications:
            return {
                'total_applications': 0,
                'rejected_count': 0,
                'ghosted_count': 0,
                'interview_count': 0,
                'offer_count': 0,
                'response_rate': 0,
                'interview_rate': 0,
                'rejection_rate': 0,
                'ghost_rate': 0
            }
        
        total = len(applications)
        rejected = len([a for a in applications if a.status == 'rejected'])
        ghosted = len([a for a in applications if a.status == 'ghosted'])
        interview = len([a for a in applications if a.status == 'interview'])
        offer = len([a for a in applications if a.status == 'offer'])
        
        responded = total - ghosted
        response_rate = (responded / total * 100) if total > 0 else 0
        interview_rate = (interview / total * 100) if total > 0 else 0
        rejection_rate = (rejected / total * 100) if total > 0 else 0
        ghost_rate = (ghosted / total * 100) if total > 0 else 0
        
        return {
            'total_applications': total,
            'rejected_count': rejected,
            'ghosted_count': ghosted,
            'interview_count': interview,
            'offer_count': offer,
            'response_rate': round(response_rate, 1),
            'interview_rate': round(interview_rate, 1),
            'rejection_rate': round(rejection_rate, 1),
            'ghost_rate': round(ghost_rate, 1)
        }
    
    def _analyze_role_performance(self, applications: List) -> List[Dict]:
        """Analisis performance per role category"""
        
        role_analysis = []
        role_counter = Counter([app.role_category for app in applications if app.role_category])
        
        for role, count in role_counter.most_common(5):
            role_apps = [app for app in applications if app.role_category == role]
            
            rejected = len([app for app in role_apps if app.status == 'rejected'])
            ghosted = len([app for app in role_apps if app.status == 'ghosted'])
            interview = len([app for app in role_apps if app.status == 'interview'])
            
            rejection_rate = (rejected / count * 100) if count > 0 else 0
            response_rate = ((count - ghosted) / count * 100) if count > 0 else 0
            interview_rate = (interview / count * 100) if count > 0 else 0
            
            role_analysis.append({
                'role': role,
                'applications': count,
                'rejected': rejected,
                'ghosted': ghosted,
                'interview': interview,
                'rejection_rate': round(rejection_rate, 1),
                'response_rate': round(response_rate, 1),
                'interview_rate': round(interview_rate, 1),
                'performance': 'good' if interview_rate > 20 else 'fair' if response_rate > 30 else 'poor'
            })
        
        return role_analysis
    
    def _detect_rejection_patterns(self, applications: List) -> List[Dict]:
        """Deteksi pola penolakan spesifik"""
        
        patterns = []
        
        if len(applications) < 2:
            return patterns
        
        stats = self._analyze_rejection_patterns(applications)
        
        # Pattern 1: Low response rate
        if stats['response_rate'] < 30:
            patterns.append({
                'type': 'low_response',
                'description': f'Response rate sangat rendah ({stats["response_rate"]}%) - resume/CV mungkin tidak menarik atau tidak sesuai',
                'severity': 'high' if stats['response_rate'] < 20 else 'medium',
                'suggested_focus': 'resume_optimization'
            })
        
        # Pattern 2: High ghosting rate
        if stats['ghost_rate'] > 50:
            patterns.append({
                'type': 'high_ghosting',
                'description': f'Tingkat ghosting tinggi ({stats["ghost_rate"]}%) - aplikasi tidak ditindaklanjuti perusahaan',
                'severity': 'high',
                'suggested_focus': 'application_strategy'
            })
        
        # Pattern 3: High rejection after interview
        if stats['interview_count'] > 0:
            rejection_after_interview = len([a for a in applications 
                                           if a.status == 'rejected' and hasattr(a, 'rejection_stage') 
                                           and 'interview' in str(a.rejection_stage).lower()])
            
            if rejection_after_interview / stats['interview_count'] > 0.5:
                patterns.append({
                    'type': 'interview_failure',
                    'description': 'Banyak penolakan setelah interview - perlu improvement interview skills',
                    'severity': 'medium',
                    'suggested_focus': 'interview_preparation'
                })
        
        # Pattern 4: Role-specific issues
        role_analysis = self._analyze_role_performance(applications)
        for role in role_analysis:
            if role['applications'] >= 2 and role['rejection_rate'] > 70:
                patterns.append({
                    'type': 'role_specific_issue',
                    'description': f'Tingkat penolakan tinggi untuk role {role["role"]} ({role["rejection_rate"]}%)',
                    'severity': 'medium',
                    'suggested_focus': 'role_targeting'
                })
        
        return patterns
    
    def _analyze_timing_patterns(self, applications: List) -> Dict:
        """Analisis pola waktu aplikasi"""
        
        if not applications:
            return {'average_time_to_response': 0, 'application_frequency': 'low'}
        
        # Hitung rata-rata waktu aplikasi
        app_dates = []
        for app in applications:
            if hasattr(app, 'date_applied'):
                try:
                    if hasattr(app.date_applied, 'date'):
                        app_dates.append(app.date_applied.date())
                    else:
                        from datetime import datetime as dt
                        app_dates.append(dt.strptime(str(app.date_applied), '%Y-%m-%d').date())
                except:
                    continue
        
        if len(app_dates) < 2:
            return {'average_time_to_response': 0, 'application_frequency': 'low'}
        
        # Analisis frekuensi aplikasi
        from datetime import datetime, timedelta
        app_dates.sort()
        date_range = (app_dates[-1] - app_dates[0]).days
        frequency = len(app_dates) / max(1, date_range) * 7  # aplikasi per minggu
        
        freq_category = 'high' if frequency > 2 else 'medium' if frequency > 0.5 else 'low'
        
        return {
            'total_applications': len(app_dates),
            'date_range_days': date_range,
            'applications_per_week': round(frequency, 1),
            'application_frequency': freq_category,
            'first_application': app_dates[0].isoformat() if app_dates else None,
            'last_application': app_dates[-1].isoformat() if app_dates else None
        }
    
    def _analyze_company_patterns(self, applications: List) -> Dict:
        """Analisis pola berdasarkan perusahaan"""
        
        company_counter = Counter([app.company for app in applications if app.company])
        
        if not company_counter:
            return {'top_companies': [], 'company_diversity': 'low'}
        
        top_companies = []
        for company, count in company_counter.most_common(5):
            company_apps = [app for app in applications if app.company == company]
            
            rejected = len([app for app in company_apps if app.status == 'rejected'])
            response_rate = ((count - len([app for app in company_apps if app.status == 'ghosted'])) / count * 100) if count > 0 else 0
            
            top_companies.append({
                'company': company,
                'applications': count,
                'rejected': rejected,
                'response_rate': round(response_rate, 1),
                'rejection_rate': round((rejected / count * 100) if count > 0 else 0, 1)
            })
        
        # Diversity analysis
        unique_companies = len(company_counter)
        total_apps = len(applications)
        diversity_score = (unique_companies / total_apps * 100) if total_apps > 0 else 0
        
        diversity_category = 'high' if diversity_score > 70 else 'medium' if diversity_score > 30 else 'low'
        
        return {
            'top_companies': top_companies,
            'unique_companies': unique_companies,
            'company_diversity_score': round(diversity_score, 1),
            'company_diversity': diversity_category
        }
    
    def _convert_insights_to_strategies(self, ai_insights: Dict, application) -> Dict[str, Any]:
        """Convert AI insights ke format strategies database dengan intelligence"""
        
        strategies = []
        pivot_suggestions = {}
        
        # Convert AI recommendations ke strategies
        recommendations = ai_insights.get('actionable_recommendations', [])
        
        for rec in recommendations[:6]:  # Max 6 strategies dari AI
            strategy = self._create_strategy_from_recommendation(rec, ai_insights)
            if strategy:
                strategies.append(strategy)
        
        # Jika AI memberikan sedikit strategies, tambahkan berdasarkan common patterns
        if len(strategies) < 3:
            strategies.extend(self._get_common_strategies(application, ai_insights))
        
        # Generate pivot suggestions berdasarkan AI analysis
        pivot_suggestions = self._generate_pivot_suggestions(ai_insights, application)
        
        return {
            'strategies': strategies,
            'pivot_suggestions': pivot_suggestions,
            'ai_insights': {
                'executive_summary': ai_insights.get('executive_summary', ''),
                'key_strengths': ai_insights.get('key_strengths', []),
                'critical_issues': ai_insights.get('critical_issues', []),
                'generated_at': ai_insights.get('generated_at', datetime.now().isoformat()),
                'model': ai_insights.get('model', 'unknown')
            }
        }
    
    def _create_strategy_from_recommendation(self, recommendation: Dict, ai_insights: Dict) -> Dict:
        """Create detailed strategy dari AI recommendation"""
        
        title = recommendation.get('title', '')
        action = recommendation.get('action', '')
        priority = recommendation.get('priority', 'medium')
        
        if not title or not action:
            return None
        
        # Determine category and type
        category = self._determine_category(title + ' ' + action)
        strategy_type = self._determine_strategy_type(category)
        
        # Extract action items
        action_items = self._extract_action_items(action)
        
        # Calculate confidence score based on AI insights quality
        confidence_score = 85
        if ai_insights.get('fallback', False):
            confidence_score = 65
        elif 'error' in ai_insights:
            confidence_score = 60
        
        # Estimate completion hours
        estimated_hours = self._estimate_completion_time(category, action_items)
        
        return {
            'strategy_type': strategy_type,
            'category': category,
            'title': title,
            'description': action,
            'action_items': action_items,
            'priority': self._priority_to_number(priority),
            'confidence_score': confidence_score,
            'estimated_completion_hours': estimated_hours,
            'status': 'pending',
            'source': 'ai_analysis'
        }
    
    def _generate_strategies_based_on_pattern(self, application, patterns):
        """Generate different strategies based on specific patterns"""
        
        strategies = []
        
        # Pattern 1: High rejection rate → Resume & Skills focus
        if patterns.get('rejection_rate', 0) > 60:
            strategies.append({
                'title': 'Deep Resume Analysis & Rewrite',
                'description': 'Complete resume overhaul due to high rejection rate',
                'category': 'resume',
                'priority': 1,
                'confidence_score': 90
            })
        
        # Pattern 2: High ghosting → Networking & Application strategy
        elif patterns.get('ghost_rate', 0) > 50:
            strategies.append({
                'title': 'Strategic Application & Follow-up System',
                'description': 'Improve application quality and follow-up process',
                'category': 'strategy', 
                'priority': 1,
                'confidence_score': 85
            })
        
        # Pattern 3: Failed interviews → Interview prep
        elif patterns.get('interview_failure_rate', 0) > 40:
            strategies.append({
                'title': 'Comprehensive Interview Preparation',
                'description': 'Mock interviews and technical practice',
                'category': 'interview',
                'priority': 1,
                'confidence_score': 88
            })
        
        return strategies
    
    def _get_common_strategies(self, application, ai_insights: Dict) -> List[Dict]:
        """Tambahkan common strategies berdasarkan best practices"""
        
        common_strategies = []
        critical_issues = ai_insights.get('critical_issues', [])
        
        # Resume strategy jika ada issue terkait resume
        if any('resume' in issue.lower() or 'cv' in issue.lower() for issue in critical_issues):
            common_strategies.append({
                'strategy_type': 'resume_revision',
                'category': 'resume',
                'title': 'Professional Resume Audit',
                'description': 'Comprehensive resume review and optimization',
                'action_items': [
                    'Get resume reviewed by 2-3 professionals',
                    'Compare with successful resumes in your field',
                    'Optimize for ATS (Applicant Tracking Systems)',
                    'Add quantifiable achievements'
                ],
                'priority': 1,
                'confidence_score': 90,
                'estimated_completion_hours': 6,
                'status': 'pending',
                'source': 'best_practice'
            })
        
        # Networking strategy jika response rate rendah
        if 'low_response' in str(critical_issues).lower():
            common_strategies.append({
                'strategy_type': 'networking',
                'category': 'network',
                'title': 'Strategic Networking',
                'description': 'Build professional connections to increase opportunities',
                'action_items': [
                    'Connect with 10 professionals in target companies on LinkedIn',
                    'Attend 2 virtual industry events this month',
                    'Request informational interviews with 3 people in desired roles',
                    'Join relevant professional groups and communities'
                ],
                'priority': 2,
                'confidence_score': 80,
                'estimated_completion_hours': 8,
                'status': 'pending',
                'source': 'best_practice'
            })
        
        # Skill development strategy umum
        common_strategies.append({
            'strategy_type': 'skill_development',
            'category': 'skills',
            'title': 'Targeted Skill Enhancement',
            'description': 'Develop skills specifically requested in job descriptions',
            'action_items': [
                'Analyze 10 recent job descriptions for your target role',
                'Identify 3 most frequently requested technical skills',
                'Complete one online course or certification',
                'Build a small project using those skills'
            ],
            'priority': 2,
            'confidence_score': 85,
            'estimated_completion_hours': 15,
            'status': 'pending',
            'source': 'best_practice'
        })
        
        return common_strategies
    
    def _generate_pivot_suggestions(self, ai_insights: Dict, application) -> Dict:
        """Generate career pivot suggestions berdasarkan AI analysis"""
        
        critical_issues = ai_insights.get('critical_issues', [])
        key_strengths = ai_insights.get('key_strengths', [])
        
        # Cek apakah perlu pivot suggestions
        needs_pivot = any(word in str(critical_issues).lower() 
                         for word in ['role', 'career', 'transition', 'change', 'pivot', 'switch'])
        
        if not needs_pivot and len(critical_issues) < 3:
            return {}
        
        # Generate pivot suggestions berdasarkan role category
        role_category = application.role_category if hasattr(application, 'role_category') else 'dev'
        
        pivot_map = {
            'dev': [
                {'title': 'Technical Product Manager', 'industry': 'Tech', 'match_score': 75},
                {'title': 'Solutions Architect', 'industry': 'Tech/Consulting', 'match_score': 70},
                {'title': 'DevOps Engineer', 'industry': 'Tech', 'match_score': 85},
                {'title': 'Data Engineer', 'industry': 'Tech', 'match_score': 65}
            ],
            'ops': [
                {'title': 'Site Reliability Engineer', 'industry': 'Tech', 'match_score': 80},
                {'title': 'Cloud Architect', 'industry': 'Tech', 'match_score': 75},
                {'title': 'IT Project Manager', 'industry': 'Various', 'match_score': 65}
            ],
            'ai': [
                {'title': 'ML Engineer', 'industry': 'Tech', 'match_score': 85},
                {'title': 'Data Scientist', 'industry': 'Various', 'match_score': 80},
                {'title': 'AI Product Manager', 'industry': 'Tech', 'match_score': 70}
            ],
            'it': [
                {'title': 'Cybersecurity Analyst', 'industry': 'Various', 'match_score': 75},
                {'title': 'Systems Administrator', 'industry': 'Various', 'match_score': 85},
                {'title': 'IT Consultant', 'industry': 'Consulting', 'match_score': 70}
            ]
        }
        
        suggested_roles = pivot_map.get(role_category, [
            {'title': 'Project Manager', 'industry': 'Various', 'match_score': 65},
            {'title': 'Business Analyst', 'industry': 'Various', 'match_score': 60}
        ])
        
        # Add reasons based on analysis
        for role in suggested_roles:
            role['reason'] = self._generate_pivot_reason(role, key_strengths)
        
        # Determine market demand
        market_demand = 'high' if role_category in ['dev', 'ai'] else 'medium'
        
        # Identify skill gaps
        common_skill_gaps = {
            'dev': ['Product Management', 'Business Strategy', 'Client Communication'],
            'ops': ['Software Development', 'Advanced Scripting', 'Cloud Architecture'],
            'ai': ['Production Deployment', 'Software Engineering', 'Business Applications'],
            'it': ['Programming', 'Cloud Technologies', 'Security Frameworks']
        }
        
        skill_gaps = common_skill_gaps.get(role_category, ['Industry-specific knowledge', 'Advanced certifications'])
        
        return {
            'suggested_roles': suggested_roles[:3],  # Max 3 suggestions
            'transferable_skills': key_strengths if key_strengths else ['Problem-solving', 'Analytical Thinking', 'Technical Knowledge'],
            'skill_gaps': skill_gaps,
            'market_demand': market_demand,
            'transition_timeline': '3-6 months',
            'salary_impact': 'neutral'  # Could be increase/decrease based on role
        }
    
    def _generate_pivot_reason(self, role: Dict, strengths: List[str]) -> str:
        """Generate reason untuk pivot suggestion"""
        
        reason_templates = [
            f"Leverages your {', '.join(strengths[:2]) if strengths else 'technical'} skills in a new context",
            "Growing demand in this field with good career progression",
            "Natural extension of your current expertise with additional learning",
            "Combines technical skills with {role_specific} aspects"
        ]
        
        import random
        template = random.choice(reason_templates)
        
        role_specific_map = {
            'Technical Product Manager': 'product strategy and business',
            'Solutions Architect': 'client-facing and architectural',
            'DevOps Engineer': 'operations and automation',
            'Data Engineer': 'data pipeline and infrastructure'
        }
        
        return template.format(
            role_specific=role_specific_map.get(role['title'], 'business and strategy')
        )
    
    def _enhance_with_pattern_analysis(self, strategies_data: Dict, analysis_data: Dict) -> Dict:
        """Enhance strategies dengan pattern analysis"""
        
        patterns = analysis_data.get('patterns', [])
        
        for pattern in patterns:
            if pattern.get('suggested_focus'):
                focus = pattern['suggested_focus']
                severity = pattern.get('severity', 'medium')
                
                # Add strategy based on pattern jika belum ada
                if focus == 'resume_optimization' and severity == 'high':
                    strategies_data['strategies'].append(self._create_resume_optimization_strategy())
                elif focus == 'interview_preparation':
                    strategies_data['strategies'].append(self._create_interview_prep_strategy())
        
        return strategies_data
    
    def _generate_pattern_based_strategies(self, application, all_applications: List) -> Dict[str, Any]:
        """Generate strategies berdasarkan pattern analysis jika AI gagal"""
        
        analysis_data = self._prepare_analysis_data(application, all_applications)
        patterns = analysis_data.get('patterns', [])
        
        strategies = []
        
        # Default strategies
        strategies.append({
            'strategy_type': 'resume_revision',
            'category': 'resume',
            'title': 'Resume Optimization',
            'description': 'Improve your resume based on application patterns',
            'action_items': [
                'Update resume with recent experiences',
                'Tailor for specific roles you\'re targeting',
                'Add measurable achievements'
            ],
            'priority': 1,
            'confidence_score': 75,
            'estimated_completion_hours': 4,
            'status': 'pending',
            'source': 'pattern_analysis'
        })
        
        # Add pattern-specific strategies
        for pattern in patterns:
            if pattern.get('type') == 'low_response':
                strategies.append({
                    'strategy_type': 'application_strategy',
                    'category': 'strategy',
                    'title': 'Improve Application Response Rate',
                    'description': pattern['description'],
                    'action_items': [
                        'Research companies before applying',
                        'Customize cover letters',
                        'Follow up after 1 week'
                    ],
                    'priority': 1,
                    'confidence_score': 80,
                    'estimated_completion_hours': 3,
                    'status': 'pending',
                    'source': 'pattern_analysis'
                })
        
        # Ensure minimum 3 strategies
        while len(strategies) < 3:
            strategies.append({
                'strategy_type': 'skill_development',
                'category': 'skills',
                'title': 'Continuous Learning',
                'description': 'Stay updated with industry trends and skills',
                'action_items': [
                    'Identify one new skill to learn each month',
                    'Complete online courses',
                    'Practice through projects'
                ],
                'priority': 2,
                'confidence_score': 70,
                'estimated_completion_hours': 10,
                'status': 'pending',
                'source': 'best_practice'
            })
        
        return {
            'strategies': strategies,
            'pivot_suggestions': self._generate_basic_pivot_suggestions(application),
            'ai_insights': {
                'executive_summary': 'Pattern-based analysis (AI service unavailable)',
                'key_strengths': ['Systematic application tracking'],
                'critical_issues': ['Using fallback analysis without AI'],
                'generated_at': datetime.now().isoformat(),
                'model': 'pattern_analysis'
            }
        }
    
    def _create_resume_optimization_strategy(self) -> Dict:
        return {
            'strategy_type': 'resume_revision',
            'category': 'resume',
            'title': 'Urgent Resume Overhaul',
            'description': 'Complete resume redesign to increase response rates',
            'action_items': [
                'Hire professional resume writer',
                'Create ATS-optimized version',
                'Develop role-specific templates',
                'Add portfolio links and projects'
            ],
            'priority': 1,
            'confidence_score': 90,
            'estimated_completion_hours': 8,
            'status': 'pending',
            'source': 'high_priority'
        }
    
    def _create_interview_prep_strategy(self) -> Dict:
        return {
            'strategy_type': 'interview_prep',
            'category': 'interview',
            'title': 'Comprehensive Interview Preparation',
            'description': 'Prepare for technical and behavioral interviews',
            'action_items': [
                'Practice 10 common technical questions',
                'Prepare 5 STAR stories for behavioral questions',
                'Do 3 mock interviews with peers',
                'Research company culture and values'
            ],
            'priority': 1,
            'confidence_score': 85,
            'estimated_completion_hours': 12,
            'status': 'pending',
            'source': 'high_priority'
        }
    
    def _generate_basic_pivot_suggestions(self, application) -> Dict:
        return {
            'suggested_roles': [
                {
                    'title': f'{application.role_category.upper()} Specialist',
                    'industry': 'Tech',
                    'match_score': 75,
                    'reason': 'Based on your current role focus'
                }
            ],
            'transferable_skills': ['Analytical Skills', 'Problem Solving', 'Technical Knowledge'],
            'skill_gaps': ['Industry-specific certifications', 'Advanced tools'],
            'market_demand': 'medium',
            'transition_timeline': '3-6 months'
        }
    
    # ==================== HELPER METHODS ====================
    
    def _determine_category(self, text: str) -> str:
        """Determine category dari teks"""
        text_lower = text.lower()
        
        category_keywords = {
            'resume': ['resume', 'cv', 'curriculum vitae', 'application document'],
            'skills': ['skill', 'learn', 'course', 'training', 'certification', 'study'],
            'interview': ['interview', 'mock', 'practice', 'question', 'answer', 'technical test'],
            'network': ['network', 'connect', 'linkedin', 'referral', 'contact', 'community'],
            'portfolio': ['portfolio', 'project', 'github', 'showcase', 'work sample'],
            'strategy': ['strategy', 'plan', 'approach', 'method', 'tactic']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return 'career_development'
    
    def _determine_strategy_type(self, category: str) -> str:
        mapping = {
            'resume': 'resume_revision',
            'skills': 'skill_development',
            'interview': 'interview_prep',
            'network': 'networking',
            'portfolio': 'portfolio_building',
            'strategy': 'application_strategy',
            'career_development': 'career_planning'
        }
        return mapping.get(category, 'career_planning')
    
    def _extract_action_items(self, text: str) -> List[str]:
        """Extract action items dari teks dengan regex yang lebih baik"""
        actions = []
        
        # Pattern untuk bullet points (•, -, *, etc.)
        bullet_patterns = [
            r'[•\-*]\s*(.+?)(?=\n|$)',
            r'\d+\.\s*(.+?)(?=\n|$)',
            r'\[x\]\s*(.+?)(?=\n|$)'
        ]
        
        for pattern in bullet_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                actions = [m.strip() for m in matches[:5]]  # Max 5 actions
                break
        
        # Jika tidak ada bullet points, split by sentences
        if not actions:
            sentences = re.split(r'[.!?]+', text)
            actions = [s.strip() for s in sentences[:3] if len(s.strip()) > 10]
        
        # Ensure minimum 2 actions
        if len(actions) < 2:
            actions = ['Implement the strategy', 'Track progress weekly', 'Review and adjust as needed']
        
        return actions[:5]  # Max 5 actions
    
    def _priority_to_number(self, priority: str) -> int:
        priority_map = {
            'critical': 1,
            'high': 1,
            'urgent': 1,
            'medium': 2,
            'normal': 2,
            'low': 3
        }
        return priority_map.get(priority.lower(), 2)
    
    def _estimate_completion_time(self, category: str, action_items: List[str]) -> int:
        """Estimate waktu penyelesaian berdasarkan kategori dan kompleksitas"""
        base_hours = {
            'resume': 3,
            'skills': 15,
            'interview': 8,
            'network': 6,
            'portfolio': 12,
            'strategy': 4,
            'career_development': 5
        }
        
        hours = base_hours.get(category, 5)
        
        # Adjust based on number of action items
        if len(action_items) > 3:
            hours += 2
        if any('course' in item.lower() or 'certification' in item.lower() for item in action_items):
            hours += 10
        
        return max(1, min(hours, 40))  # Cap antara 1-40 jam
    
    def _get_default_strategies(self, application) -> Dict[str, Any]:
        """Comprehensive default strategies"""
        return {
            'strategies': [
                {
                    'strategy_type': 'resume_revision',
                    'category': 'resume',
                    'title': 'Resume Enhancement',
                    'description': 'Improve your resume for better response rates',
                    'action_items': [
                        'Update with recent experiences',
                        'Add quantifiable achievements',
                        'Tailor for target roles'
                    ],
                    'priority': 1,
                    'confidence_score': 80,
                    'estimated_completion_hours': 4,
                    'status': 'pending',
                    'source': 'default'
                },
                {
                    'strategy_type': 'skill_development',
                    'category': 'skills',
                    'title': 'Skill Building',
                    'description': 'Develop in-demand skills for your target roles',
                    'action_items': [
                        'Identify key skills from job descriptions',
                        'Find relevant courses or tutorials',
                        'Practice through projects'
                    ],
                    'priority': 2,
                    'confidence_score': 75,
                    'estimated_completion_hours': 10,
                    'status': 'pending',
                    'source': 'default'
                }
            ],
            'pivot_suggestions': {},
            'ai_insights': {
                'executive_summary': 'Default strategies (AI analysis unavailable)',
                'key_strengths': ['Application tracking in place'],
                'critical_issues': ['AI service not configured or unavailable'],
                'generated_at': datetime.now().isoformat(),
                'model': 'default'
            }
        }