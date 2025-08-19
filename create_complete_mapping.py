import json

# Load raw data
with open('raw_mXFHAmih.json', 'r', encoding='utf-8') as f:
    responses = json.load(f)

if responses:
    first_response = responses[0]
    answers = first_response.get('answers', [])
    
    # Create mapping based on the original question mapping order
    # We'll assume the answers are in the same order as Q1-Q32
    original_mapping = {
        "Q1": "Strategic Connection - Alignment with business strategy",
        "Q2": "Strategic Connection - Leadership support for learning", 
        "Q3": "Strategic Connection - Future capability planning",
        "Q4": "Strategic Connection - Business stakeholder input",
        "Q5": "Needs Analysis - Prioritization by impact",
        "Q6": "Needs Analysis - Data and discussion mix",
        "Q7": "Needs Analysis - Ongoing analysis process", 
        "Q8": "Needs Analysis - Insights drive decisions",
        "Q9": "Learning Design - Tailored to learner needs",
        "Q10": "Learning Design - Content relevance and quality",
        "Q11": "Learning Design - Engaging delivery formats",
        "Q12": "Learning Design - Practical application",
        "Q13": "Learning Culture - Psychological safety",
        "Q14": "Learning Culture - Manager support for learning",
        "Q15": "Learning Culture - Time/space for learning",
        "Q16": "Learning Culture - Shared responsibility",
        "Q17": "Platform and Tools - Ease of navigation",
        "Q18": "Platform and Tools - Integration with daily work", 
        "Q19": "Platform and Tools - Insightful data usage",
        "Q20": "Platform and Tools - Modern, relevant tools",
        "Q21": "Integration with Talent - Learning-to-career connection",
        "Q22": "Integration with Talent - Performance-driven development",
        "Q23": "Integration with Talent - Role in succession planning",
        "Q24": "Integration with Talent - Integration with HR systems",
        "Q25": "Learning Impact - Beyond attendance tracking",
        "Q26": "Learning Impact - Connection to business metrics",
        "Q27": "Learning Impact - Observed behavior change",
        "Q28": "Learning Impact - Continuous feedback loop",
        "Q29": "Future Capability - Future skill planning",
        "Q30": "Future Capability - Trend-based strategy",
        "Q31": "Future Capability - Supports growth mindset",
        "Q32": "Future Capability - Capability roadmap"
    }
    
    # Create new mapping with actual field IDs
    new_mapping = {}
    
    print("=== Creating Field ID Mapping ===")
    for i, answer in enumerate(answers):
        field_id = answer['field']['id']
        if i < len(original_mapping):
            q_key = f"Q{i+1}"
            element_subelement = original_mapping[q_key]
            element, subelement = element_subelement.split(" - ", 1)
            
            new_mapping[field_id] = {
                "element": element,
                "subelement": subelement
            }
            print(f"Answer {i+1}: {field_id} -> {element} - {subelement}")
    
    # Save the new mapping
    with open('question_mapping_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(new_mapping, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== Saved {len(new_mapping)} mappings to question_mapping_fixed.json ===")
    print("You can now use this mapping to process the raw data correctly.") 