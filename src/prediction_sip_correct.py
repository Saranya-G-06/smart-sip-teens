import joblib
import numpy as np
import pandas as pd

def predict_sip_for_teen(age, monthly_allowance, financial_literacy_score, 
                         risk_appetite, sip_amount, fund_category, fund_risk_category):
    """
    Predict SIP recommendation for a teen using the trained model
    
    Parameters:
    -----------
    age: int (13-19)
    monthly_allowance: int (monthly allowance in INR)
    financial_literacy_score: float (1-10)
    risk_appetite: str ('Low', 'Medium', 'High')
    sip_amount: int (proposed SIP amount in INR)
    fund_category: str ('Equity', 'Debt', 'Hybrid', 'Liquid')
    fund_risk_category: str ('Low', 'Medium', 'High')
    
    Returns:
    --------
    dict: Prediction results with explanation
    """
    
    # Load model artifacts
    model = joblib.load('models/best_sip_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    label_encoders = joblib.load('models/label_encoders.pkl')
    feature_names = joblib.load('models/feature_names.pkl')
    
    # Create a DataFrame with the input data
    input_data = {
        'age': age,
        'monthly_allowance': monthly_allowance,
        'financial_literacy_score': financial_literacy_score,
        'sip_amount': sip_amount,
    }
    
    # Encode categorical variables
    for col, le in label_encoders.items():
        col_name = f"{col}_encoded"
        try:
            input_data[col_name] = le.transform([locals()[col]])[0]
        except ValueError:
            # Handle unseen labels by using the most common
            input_data[col_name] = le.transform([le.classes_[0]])[0]
    
    # Ensure all feature names are present
    for feature in feature_names:
        if feature not in input_data:
            input_data[feature] = 0  # Default value for missing features
    
    # Create feature array in correct order
    X = np.array([[input_data[feature] for feature in feature_names]])
    
    # Scale features
    X_scaled = scaler.transform(X)
    
    # Predict
    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0][prediction]
    
    # Get feature importance if available
    feature_importance = {}
    if hasattr(model, 'feature_importances_'):
        for i, feature in enumerate(feature_names):
            feature_importance[feature] = model.feature_importances_[i]
    
    # Generate explanation
    explanation = generate_explanation(prediction, probability, input_data, feature_importance)
    
    # Prepare result
    result = {
        'prediction': int(prediction),
        'probability': float(probability),
        'recommendation': 'RECOMMEND SIP' if prediction == 1 else 'NOT RECOMMEND SIP',
        'confidence': f"{probability:.1%}",
        'explanation': explanation,
        'input_features': input_data
    }
    
    return result

def generate_explanation(prediction, probability, input_data, feature_importance):
    """Generate human-readable explanation for the prediction"""
    
    explanations = []
    
    # Rule-based explanations
    if prediction == 1:
        explanations.append("✅ This teen-profile combination is suitable for SIP investment.")
    else:
        explanations.append("❌ This teen-profile combination is not suitable for SIP investment.")
    
    # Add specific feature-based explanations
    if input_data.get('financial_literacy_score', 0) < 5:
        explanations.append("⚠️  Low financial literacy score detected.")
    
    if input_data.get('sip_amount', 0) > input_data.get('monthly_allowance', 1) * 0.3:
        explanations.append("⚠️  SIP amount exceeds 30% of monthly allowance (generally not recommended).")
    
    if input_data.get('age', 18) < 16:
        explanations.append("📝 Note: Young age suggests need for parental guidance.")
    
    # Add top features if available
    if feature_importance:
        top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
        explanations.append(f"🔑 Top influencing factors: {', '.join([f[0].replace('_encoded', '') for f in top_features])}")
    
    return explanations

def interactive_demo():
    """Interactive demo for viva presentation"""
    
    print("🎯 SMART SIP RECOMMENDATION SYSTEM FOR TEENS")
    print("="*60)
    print("Interactive Demo for Final Year Project Viva")
    print("="*60)
    
    # Sample teen profiles for demonstration
    sample_profiles = [
        {
            'name': 'Rahul',
            'age': 17,
            'monthly_allowance': 3000,
            'financial_literacy_score': 7.5,
            'risk_appetite': 'Medium',
            'sip_amount': 1000,
            'fund_category': 'Hybrid',
            'fund_risk_category': 'Medium'
        },
        {
            'name': 'Priya',
            'age': 15,
            'monthly_allowance': 1500,
            'financial_literacy_score': 4.0,
            'risk_appetite': 'Low',
            'sip_amount': 800,
            'fund_category': 'Debt',
            'fund_risk_category': 'Low'
        },
        {
            'name': 'Arjun',
            'age': 19,
            'monthly_allowance': 5000,
            'financial_literacy_score': 8.5,
            'risk_appetite': 'High',
            'sip_amount': 2000,
            'fund_category': 'Equity',
            'fund_risk_category': 'High'
        }
    ]
    
    for profile in sample_profiles:
        print(f"\n{'='*60}")
        print(f"🧑‍🎓 TEEN PROFILE: {profile['name']}")
        print(f"{'='*60}")
        
        print(f"\n📋 Profile Details:")
        print(f"   Age: {profile['age']} years")
        print(f"   Monthly Allowance: ₹{profile['monthly_allowance']}")
        print(f"   Financial Literacy: {profile['financial_literacy_score']}/10")
        print(f"   Risk Appetite: {profile['risk_appetite']}")
        print(f"   Proposed SIP Amount: ₹{profile['sip_amount']}")
        print(f"   Fund Category: {profile['fund_category']}")
        print(f"   Fund Risk: {profile['fund_risk_category']}")
        
        print(f"\n🤖 Making Prediction...")
        result = predict_sip_for_teen(**{k: v for k, v in profile.items() if k != 'name'})
        
        print(f"\n📊 RESULT:")
        print(f"   Recommendation: {result['recommendation']}")
        print(f"   Confidence Level: {result['confidence']}")
        
        print(f"\n💡 Explanation:")
        for exp in result['explanation']:
            print(f"   • {exp}")
    
    # Interactive mode
    print(f"\n{'='*60}")
    print("🕹️  INTERACTIVE MODE")
    print(f"{'='*60}")
    
    while True:
        try:
            print(f"\nEnter teen details (or type 'exit' to quit):")
            
            age = int(input("Age (13-19): "))
            monthly_allowance = int(input("Monthly Allowance (₹): "))
            financial_literacy_score = float(input("Financial Literacy Score (1-10): "))
            risk_appetite = input("Risk Appetite (Low/Medium/High): ")
            sip_amount = int(input("Proposed SIP Amount (₹): "))
            fund_category = input("Fund Category (Equity/Debt/Hybrid/Liquid): ")
            fund_risk_category = input("Fund Risk Category (Low/Medium/High): ")
            
            print(f"\n🤖 Processing...")
            result = predict_sip_for_teen(
                age, monthly_allowance, financial_literacy_score,
                risk_appetite, sip_amount, fund_category, fund_risk_category
            )
            
            print(f"\n📊 RESULT:")
            print(f"   Recommendation: {result['recommendation']}")
            print(f"   Confidence: {result['confidence']}")
            
            print(f"\n💡 Explanation:")
            for exp in result['explanation']:
                print(f"   • {exp}")
                
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
            continue
        except KeyboardInterrupt:
            print(f"\n\n👋 Exiting demo. Good luck with your viva!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break

if __name__ == "__main__":
    interactive_demo()