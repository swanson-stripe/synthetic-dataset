# EduTech Academy Online Education Marketplace - Synthetic Data Generator

Generate realistic Stripe payment data for an online education platform with instructor payouts, student financing, and corporate training programs.

## 🎓 Business Model

EduTech Academy simulates a comprehensive online education marketplace that:
- **Connects instructors** with students through course sales
- **Manages payments** with 70/30 revenue sharing (instructor/platform)
- **Offers financing** with 0% APR payment plans for expensive courses
- **Serves corporate clients** with bulk training and volume discounts
- **Processes refunds** within 30-day satisfaction guarantees

## 🏗️ Platform Features

### Core Marketplace
- **Multi-category courses**: Technology, Business, Design, Languages, Arts
- **Flexible pricing tiers**: Mini ($9-29), Standard ($49-99), Comprehensive ($199-499), Bootcamp ($999-2999)
- **Payment options**: One-time payments and installment plans
- **Corporate training**: Bulk enrollments with volume discounts
- **Refund protection**: 30-day money-back guarantee

### Stripe Products Used
- **Connect**: Instructor onboarding with Express accounts
- **Capital**: Student financing for expensive courses (0% APR)
- **Billing**: Subscription-based payment plans
- **Invoicing**: Corporate training with net payment terms
- **Refunds**: Automated refund processing with instructor clawbacks

## 📊 Generated Data Structure

### Core Entities
- **Instructors**: 72 Expert accounts across 5 categories
- **Students**: 73,656 individual learners and professionals
- **Courses**: 218 courses with realistic pricing and ratings
- **Enrollments**: 12,511 individual enrollments plus corporate bulk
- **Corporate Accounts**: 3 companies with training programs

### Revenue Distribution
- **Total Marketplace Revenue**: $201.4M over 24 months
- **Individual Student Revenue**: $197.9M (98.3%)
- **Corporate Training Revenue**: $3.5M (1.7%)
- **Platform Revenue**: $60.4M (30% share)
- **Instructor Earnings**: $141.0M (70% share)

## 💰 Financial Patterns

### Revenue Sharing
- **Instructor Share**: 70% of course sales
- **Platform Share**: 30% for payment processing and marketing
- **Payment Plans**: 0% APR financing for courses over $500
- **Corporate Discounts**: 10-30% based on employee count

### Course Pricing Strategy
- **Mini Courses**: $9-29 (introductory content)
- **Standard Courses**: $49-99 (comprehensive learning)
- **Comprehensive**: $199-499 (professional development)
- **Bootcamps**: $999-2999 (intensive career programs)

## 🎯 Student Financing

### Payment Plan Options
- **Eligibility**: Courses over $500 with 40% uptake
- **Terms**: 2, 3, 4, or 6 monthly installments
- **Interest Rate**: 0% APR (platform absorption)
- **Usage**: 68 financing agreements generated

### Corporate Training
- **Volume Discounts**: 10% (small), 20% (medium), 30% (large)
- **Payment Terms**: Net 30 invoicing
- **Bulk Enrollment**: 5-50 employees per course
- **Industry Focus**: Technology, Healthcare, Finance

## 🔄 Refund Management

### Refund Policy
- **Window**: 30-day money-back guarantee
- **Rate**: 4.4% of enrollments (varies by stage)
- **Processing**: Automatic refund with instructor clawback
- **Reasons**: Course quality, technical issues, not as described

### Instructor Impact
- **Revenue Reversal**: Instructor share reversed on refunds
- **Quality Incentive**: Lower refund rates improve instructor rankings
- **Support**: Platform assists with student satisfaction

## 📁 Output Files

### Core Marketplace Data
- `instructors.json` - Express accounts with expertise and ratings
- `students.json` - Customer profiles with learning preferences
- `courses.json` - Course catalog with pricing and metadata
- `enrollments.json` - Individual and corporate enrollment records

### Financial Data
- `instructor_transfers.json` - Revenue payouts to instructors
- `refunds.json` - Refund processing and reversals
- `student_financing.json` - Payment plan agreements
- `corporate_accounts.json` - Corporate training customers

### Learning Analytics & Compliance
- `student_progress.json` - Learning analytics and course completion data
- `tax_documents.json` - 1099-K and international tax reporting
- `education_metrics.json` - Platform performance and trends

## 🚀 Usage

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Generate data
python generate_edutech.py
```

### Sample Output
```
📊 GENERATION SUMMARY:
   Total instructors: 72
   Total students: 73,656
   Total courses: 218
   Individual enrollments: 12,511
   Corporate accounts: 3

💰 REVENUE METRICS:
   Total marketplace revenue: $201,440,820.00
   Platform revenue (30%): $60,432,246.00
   Instructor earnings (70%): $141,008,574.00
   Revenue per student: $2,734.89
   Revenue per instructor: $1,958,452.42

📚 LEARNING ANALYTICS:
   Course completion rate: 31.2%
   Average satisfaction: 4.0/5.0
   Certificates earned: 95
   Progress records: 1,000

📋 TAX COMPLIANCE:
   Tax documents issued: 72
   Total taxable earnings: $133,573,841.00
```

## 🎨 Course Categories

### Distribution
- **Technology**: 40.8% (89 courses) - Programming, data science, cybersecurity
- **Business**: 22.5% (49 courses) - Marketing, leadership, finance
- **Design**: 21.1% (46 courses) - UI/UX, graphic design, video editing
- **Languages**: 10.6% (23 courses) - Spanish, French, Mandarin
- **Arts**: 5.0% (11 courses) - Music, writing, digital art

### Instructor Expertise
- **Credentials**: PhD, Masters, Professional, Industry Expert
- **Experience**: 1-15 years teaching
- **Ratings**: 4.0-5.0 average student rating
- **Completion Rates**: 60-95% course completion

## 📈 Key Metrics Tracked

### Financial Performance
- **Marketplace GMV**: Total gross merchandise value
- **Revenue per Student**: Average lifetime value per learner
- **Payment Plan Adoption**: Financing usage for expensive courses
- **Corporate Penetration**: Enterprise training market share

### Operational Efficiency
- **Instructor Retention**: Revenue per instructor trends
- **Course Performance**: Enrollment and completion rates
- **Refund Management**: Satisfaction and quality metrics
- **Platform Growth**: Student acquisition and engagement

## 🎯 Use Cases

### Product Development
- **Payment flow optimization**: Test financing vs one-time payments
- **Instructor onboarding**: Revenue sharing and payout strategies
- **Corporate sales**: Bulk enrollment and volume pricing
- **Quality assurance**: Refund pattern analysis

### Data Analysis
- **Student behavior**: Course selection and completion patterns
- **Instructor performance**: Revenue generation and student satisfaction
- **Market trends**: Category growth and pricing optimization
- **Financial modeling**: Revenue projections and margin analysis

## 📚 Learning Analytics Features

### Student Progress Tracking
- **Completion Rates**: Course completion percentages and timing
- **Engagement Metrics**: Time spent, assignments completed, quiz scores
- **Certificate Generation**: Automatic certificates for eligible courses
- **Satisfaction Ratings**: Student feedback and course ratings

### Instructor Performance
- **Revenue Analytics**: Earnings, refund rates, student satisfaction
- **Course Metrics**: Completion rates, enrollment trends, pricing optimization
- **Quality Indicators**: Refund rates correlated with course quality

## 📋 Tax Compliance System

### 1099-K Generation
- **IRS Threshold**: Automatic 1099-K for instructors earning >$600
- **Electronic Delivery**: Digital tax document distribution
- **Annual Reporting**: Complete year-end tax compliance
- **International Support**: Tax treaty handling for global instructors

### Compliance Features
- **Gross Earnings Tracking**: Complete instructor revenue reporting
- **Transaction Counting**: Payment volume for tax requirements
- **Withholding Calculation**: International tax withholding rates
- **Delivery Confirmation**: Electronic document delivery tracking

## ⚡ Performance

- **Generation Time**: ~14.1 seconds
- **Data Volume**: 12,511 enrollments + 1,000 progress records + 72 tax documents
- **Revenue Scale**: $201M+ in marketplace transactions
- **Student Scale**: 73K+ learners with detailed analytics
- **File Count**: 11 comprehensive JSON outputs

## 🔒 Data Privacy

All generated data is synthetic and contains no real PII:
- Fake instructor and student profiles using Faker library
- Generated email addresses and contact information
- Simulated payment methods and financial details
- Synthetic course content and descriptions

Perfect for prototyping education platforms without privacy concerns.
