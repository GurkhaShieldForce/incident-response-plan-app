from flask import Flask, render_template, jsonify, request, abort
from flask_cors import CORS
import logging
from datetime import datetime
import os


app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(filename='irp_app.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


irp_data = {
    "phases": [
        {"id": "preparation", "name": "Preparation", "color": "bg-green-500"},
        {"id": "detection", "name": "Detection", "color": "bg-orange-500"},
        {"id": "analysis", "name": "Analysis", "color": "bg-yellow-500"},
        {"id": "containment", "name": "Containment", "color": "bg-red-500"},
        {"id": "eradication", "name": "Eradication", "color": "bg-red-700"},
        {"id": "recovery", "name": "Recovery", "color": "bg-blue-500"},
        {"id": "post-incident", "name": "Post Incident Actions", "color": "bg-purple-500"}
    ],
    "phaseContent": {
        "preparation": [
            "Important Notice",
            "References",
            "CIRT Personnel",
            "Playbook Activated",
            "Schedule Stand Ups"
        ],
        "detection": [
            "Source of Incident Reporting",
            "Notify Service Desk",
            "Recording Incident Information",
            "Alert CIRT of the cyber incident",
            "Collect Incident Details"
        ],
        "analysis": [
            "Review Incident Details",
            "Confirm Incident Status",
            "Document as Non-Incident",
            "Confidential information assessment",
            "Privacy Breach Response",
            "Serious Harm Assessment"
        ],
        "containment": [
            "Contain the Incident",
            "Review Evidence to Determine Impact of Incident",
            "Prioritisation and Assessment",
            "Confirm whether 3rd parties are involved",
            "External Counsel/ Incident Response Firm assessment",
            "Engage Incident Response Firm"
        ],
        "eradication": [
            "Eradication"
        ],
        "recovery": [
            "Recovery",
            "Issue Final Incident Report"
        ],
        "post-incident": [
            "Conduct Lessons Learned Session"
        ]
    },
     "activityDetails": {
        "Important Notice": {
            "description": "This step involves notifying key stakeholders about the incident.",
            "procedures": [
                "Identify the list of key stakeholders to be notified",
                "Draft a concise but informative notice about the incident",
                "Use pre-approved templates for different types of incidents",
                "Ensure the notice includes initial assessment and next steps",
                "Distribute the notice through appropriate channels (email, SMS, etc.)",
                "Confirm receipt of the notice by all stakeholders"
            ]
        },
        "References": {
            "description": "Gather and organize all relevant reference materials for the incident response.",
            "procedures": [
                "Locate and access the Incident Response Plan document",
                "Identify relevant regulatory compliance documents",
                "Gather any specific incident handling procedures",
                "Compile contact information for all team members and external resources",
                "Ensure access to network diagrams and system inventories",
                "Prepare any necessary legal or regulatory reporting templates"
            ]
        },
        "CIRT Personnel": {
            "description": "Assemble and brief the Computer Incident Response Team (CIRT).",
            "procedures": [
                "Identify and contact all necessary CIRT members",
                "Conduct an initial briefing on the incident",
                "Assign roles and responsibilities to team members",
                "Ensure all team members have necessary access and tools",
                "Establish communication channels for the team",
                "Set up a schedule for regular check-ins and updates"
            ]
        },
        "Playbook Activated": {
            "description": "Initiate the appropriate incident response playbook based on the type of incident.",
            "procedures": [
                "Identify the type of incident (e.g., malware, data breach, DDoS)",
                "Locate and activate the corresponding incident playbook",
                "Review the playbook steps with the CIRT",
                "Assign tasks from the playbook to team members",
                "Establish timelines for each playbook step",
                "Set up a system to track progress through the playbook"
            ]
        },
        "Schedule Stand Ups": {
            "description": "Organize regular stand-up meetings to keep the team aligned and informed.",
            "procedures": [
                "Determine the frequency of stand-up meetings (e.g., daily, twice daily)",
                "Set a consistent time and virtual meeting space for stand-ups",
                "Create an agenda template for stand-up meetings",
                "Assign a facilitator for the stand-up meetings",
                "Establish rules for brief, focused updates from each team member",
                "Set up a system to record and distribute stand-up notes and action items"
            ]
        },
        "Source of Incident Reporting": {
            "description": "Identify and document the initial source of the incident report.",
            "procedures": [
                "Record the name and contact information of the person reporting the incident",
                "Document the date and time the incident was first reported",
                "Capture the initial description of the incident as reported",
                "Determine if the source is internal (employee, system alert) or external (customer, partner)",
                "Assess the credibility and urgency of the report",
                "Initiate preliminary documentation of the incident"
            ]
        },
        "Notify Service Desk": {
            "description": "Inform the service desk about the incident to coordinate support efforts.",
            "procedures": [
                "Contact the service desk supervisor or on-duty personnel",
                "Provide a brief summary of the incident",
                "Instruct on any immediate actions required from the service desk",
                "Establish a protocol for escalating related calls or tickets",
                "Request the creation of a master incident ticket if not already done",
                "Ensure the service desk is prepared to handle inquiries related to the incident"
            ]
        },
        "Recording Incident Information": {
            "description": "Document all relevant information about the incident in a structured manner.",
            "procedures": [
                "Use a standardized incident recording template or system",
                "Record the incident identification number",
                "Document the nature and scope of the incident",
                "Note all affected systems, networks, or data",
                "Log all actions taken and by whom",
                "Maintain a timeline of events related to the incident"
            ]
        },
        "Alert CIRT of the cyber incident": {
            "description": "Formally notify the Computer Incident Response Team about the cyber incident.",
            "procedures": [
                "Use the established CIRT notification protocol",
                "Provide a concise summary of the incident",
                "Specify the urgency and potential impact of the incident",
                "Request immediate actions or responses if needed",
                "Provide information on how to access the incident documentation",
                "Confirm receipt of the alert from all CIRT members"
            ]
        },
        "Collect Incident Details": {
            "description": "Gather comprehensive information about the incident to support analysis and response.",
            "procedures": [
                "Interview relevant personnel involved in or aware of the incident",
                "Collect logs from affected systems and security devices",
                "Capture screenshots or other visual evidence if applicable",
                "Document the chronology of events leading up to and following the incident",
                "Gather any relevant emails, messages, or other communications",
                "Compile a list of all potentially affected assets (hardware, software, data)"
            ]
        },
        "Review Incident Details": {
            "description": "Analyze the collected information to understand the nature and scope of the incident.",
            "procedures": [
                "Examine all collected logs, reports, and documentation",
                "Identify any patterns or anomalies in the data",
                "Cross-reference information from different sources",
                "Determine the initial vector of the incident (if known)",
                "Assess the potential impact on systems, data, and operations",
                "Identify any gaps in the collected information that need further investigation"
            ]
        },
        "Confirm Incident Status": {
            "description": "Validate whether the reported issue is indeed a security incident requiring full response.",
            "procedures": [
                "Review the incident criteria as defined in the incident response plan",
                "Compare the collected information against these criteria",
                "Consult with subject matter experts if necessary",
                "Determine if the event meets the threshold for a full incident response",
                "If confirmed, escalate to appropriate response level",
                "If not confirmed, document reasoning and consider it for future reference"
            ]
        },
        "Document as Non-Incident": {
            "description": "If the event is determined not to be a security incident, properly document and close the case.",
            "procedures": [
                "Summarize the reasons why the event does not qualify as an incident",
                "Document all steps taken in the investigation",
                "Record any recommendations for preventing similar false alarms",
                "Update relevant logs and ticketing systems",
                "Notify all involved parties of the outcome",
                "Archive the documentation for future reference"
            ]
        },
        "Confidential information assessment": {
            "description": "Evaluate whether any confidential information was compromised during the incident.",
            "procedures": [
                "Identify all systems and data potentially affected by the incident",
                "Review the classification of the affected data",
                "Determine if any confidential or sensitive information was accessed or exfiltrated",
                "Assess the potential impact of the confidential information exposure",
                "Document the scope and nature of any confidential information compromise",
                "Prepare for necessary notifications if confidential data was breached"
            ]
        },
        "Privacy Breach Response": {
            "description": "Initiate specific response procedures if personal or private information was compromised.",
            "procedures": [
                "Identify the type and extent of private information affected",
                "Determine the number of individuals whose privacy may have been breached",
                "Assess the potential harm or impact on affected individuals",
                "Prepare notifications for affected individuals as required by law",
                "Coordinate with legal team on regulatory reporting requirements",
                "Develop a communication plan for addressing privacy concerns"
            ]
        },
        "Serious Harm Assessment": {
            "description": "Evaluate the potential for serious harm resulting from the incident.",
            "procedures": [
                "Define criteria for 'serious harm' in the context of the incident",
                "Assess the potential financial impact on the organization and stakeholders",
                "Evaluate possible reputational damage",
                "Consider any physical or safety risks resulting from the incident",
                "Analyze the long-term consequences of the incident",
                "Prepare a report detailing the serious harm assessment findings"
            ]
        },
        "Contain the Incident": {
            "description": "Implement measures to prevent the incident from spreading or causing further damage.",
            "procedures": [
                "Identify the affected systems and networks",
                "Isolate compromised systems from the network",
                "Block malicious IP addresses or domains",
                "Disable compromised user accounts",
                "Apply emergency patches or configuration changes if necessary",
                "Monitor for any attempts to circumvent containment measures"
            ]
        },
        "Review Evidence to Determine Impact of Incident": {
            "description": "Analyze collected evidence to assess the full impact of the incident.",
            "procedures": [
                "Examine system logs, network traffic data, and other relevant information",
                "Identify all affected systems, applications, and data",
                "Determine the duration of the incident (when it started and if it's ongoing)",
                "Assess any data loss or unauthorized access",
                "Evaluate the operational impact on business processes",
                "Prepare a comprehensive impact assessment report"
            ]
        },
        "Prioritisation and Assessment": {
            "description": "Evaluate and prioritize response actions based on the incident's impact and urgency.",
            "procedures": [
                "Use established criteria to assess the severity of the incident",
                "Determine the potential business impact if not addressed promptly",
                "Consider any regulatory or compliance implications",
                "Prioritize response actions based on criticality and available resources",
                "Develop a timeline for implementing prioritized actions",
                "Communicate priorities and assessments to relevant stakeholders"
            ]
        },
        "Confirm whether 3rd parties are involved": {
            "description": "Determine if any third-party vendors, partners, or systems are involved in or affected by the incident.",
            "procedures": [
                "Review system interconnections and data flows with third parties",
                "Check if any third-party systems or services were used as attack vectors",
                "Assess if any third-party data or systems were compromised",
                "Determine contractual obligations related to incident reporting",
                "Prepare notifications for affected third parties",
                "Coordinate response efforts with involved third parties if necessary"
            ]
        },
        "External Counsel/ Incident Response Firm assessment": {
            "description": "Evaluate the need for external legal counsel or specialized incident response support.",
            "procedures": [
                "Assess the complexity and scope of the incident",
                "Determine if the incident exceeds internal capabilities",
                "Review agreements with pre-selected external firms",
                "Evaluate potential legal implications that require expert advice",
                "Prepare a briefing for external counsel or response firm",
                "Decide on the extent of external involvement needed"
            ]
        },
        "Engage Incident Response Firm": {
            "description": "Formally engage external incident response support if deemed necessary.",
            "procedures": [
                "Contact the chosen incident response firm",
                "Provide a comprehensive briefing on the incident",
                "Define the scope of work and expectations",
                "Establish communication protocols and reporting lines",
                "Ensure necessary access and permissions are granted",
                "Integrate external team with internal response efforts"
            ]
        },
        "Eradication": {
            "description": "Remove the cause of the incident and eliminate any remaining threats.",
            "procedures": [
                "Identify and remove malware or other malicious elements",
                "Close any vulnerabilities that were exploited",
                "Reset compromised credentials",
                "Apply necessary patches and updates",
                "Conduct a thorough sweep for any remaining threats",
                "Verify that all known threat elements have been eliminated"
            ]
        },
        "Recovery": {
            "description": "Restore affected systems and return to normal operations.",
            "procedures": [
                "Restore systems from clean backups",
                "Verify the integrity of restored data and systems",
                "Implement additional security controls as needed",
                "Gradually reintroduce restored systems to the production environment",
                "Monitor systems closely for any signs of recurring issues",
                "Update documentation with new security measures implemented"
            ]
        },
        "Issue Final Incident Report": {
            "description": "Compile and distribute a comprehensive report on the incident and response efforts.",
            "procedures": [
                "Summarize the incident timeline and key events",
                "Detail the impact assessment and damage report",
                "Outline all actions taken during the response",
                "Document lessons learned and areas for improvement",
                "Provide recommendations for preventing similar incidents",
                "Distribute the report to appropriate stakeholders and management"
            ]
        },
        "Conduct Lessons Learned Session": {
            "description": "Facilitate a post-incident review to improve future response capabilities.",
            "procedures": [
                "Schedule a meeting with all involved parties",
                "Review the incident timeline and response actions",
                "Identify what worked well and areas for improvement",
                "Discuss any new threats or vulnerabilities discovered",
                "Propose updates to the incident response plan and procedures",
                "Assign action items for implementing improvements"
            ]
        }
        
    },
        "teamRoles": [
        {
            "role": "Incident Response Manager",
            "responsibilities": [
                "Oversees the entire incident response process",
                "Makes critical decisions during incident handling",
                "Communicates with senior management"
            ]
        },
        {
            "role": "Technical Lead",
            "responsibilities": [
                "Directs technical aspects of the response",
                "Performs deep analysis of incidents",
                "Recommends containment and eradication strategies"
            ]
        },
        {
            "role": "Communications Coordinator",
            "responsibilities": [
                "Manages internal and external communications",
                "Prepares status updates and reports",
                "Liaises with legal and PR teams as needed"
            ]
        },
        {
            "role": "Security Analyst",
            "responsibilities": [
                "Monitors security systems for incidents",
                "Performs initial triage and analysis",
                "Assists in containment and eradication efforts"
            ]
        }
    ]
}
            



@app.route('/')
def index():
    return render_template('index.html', irp_data=irp_data)

@app.route('/api/activity/<activity_name>')
def get_activity_details(activity_name):
    details = irp_data['activityDetails'].get(activity_name, {})
    if not details:
        abort(404, description="Activity not found")
    return jsonify(details)

@app.route('/api/phases')
def get_phases():
    return jsonify(irp_data['phases'])

@app.route('/api/phase/<phase_id>')
def get_phase_content(phase_id):
    content = irp_data['phaseContent'].get(phase_id, [])
    if not content:
        abort(404, description="Phase not found")
    return jsonify(content)

@app.route('/api/team-roles')
def get_team_roles():
    return jsonify(irp_data['teamRoles'])

@app.route('/api/log', methods=['POST'])
def log_action():
    data = request.json
    if not data or 'action' not in data:
        abort(400, description="Invalid request")
    
    action = data['action']
    timestamp = datetime.now().isoformat()
    logging.info(f"User Action: {action} at {timestamp}")
    return jsonify({"status": "logged"}), 200

@app.errorhandler(404)
def not_found_error(error):
    logging.error(f"404 error: {error}")
    return jsonify(error=str(error)), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(f"500 error: {error}")
    return jsonify(error="Internal server error"), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001)) #Running on PORT 5001
    app.run(host='0.0.0.0', port=port, debug=True)
