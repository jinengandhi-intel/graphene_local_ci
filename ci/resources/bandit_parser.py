import re

#bandit report metrics baseline values
#NOTE add empty string after element in the tuple as regex is returning empty string after every match
# current baseline values
# Run metrics:
#        Total issues (by severity):
#                Undefined: 0
#                Low: 48
#                Medium: 0
#                High: 2
#        Total issues (by confidence):
#                Undefined: 0
#                Low: 0
#                Medium: 2
#                High: 48

baseline_metric_values = """
Total issues (by severity):
		Undefined: 0
		Low: 48
		Medium: 0
		High: 2
	Total issues (by confidence):
		Undefined: 0
		Low: 0
		Medium: 2
		High: 48
Files skipped (0):
"""
severity_baseline_values=('', '0', '', '48', '', '0', '', '2')
confidence_baseline_values=('', '0', '', '0', '', '2', '', '48')


f = open('gramine.txt','r')
contents = f.read()

bandit_analysis_report = re.search("Total issues .by severity.:\s*(.*)Undefined: (\d+)\s*(.*)Low: (\d+)\s*(.*)Medium: (\d+)\s*(.*)High: (\d+)\s*(.*)", contents, re.DOTALL)
print('Baseline gramine bandit scan report: \n' + baseline_metric_values)
print('Current build gramine bandit analysis scan report: \n\n' + bandit_analysis_report.group())

severity_regex = "Total issues .by severity.:\s*(.*)Undefined: (\d+)\s*(.*)Low: (\d+)\s*(.*)Medium: (\d+)\s*(.*)High: (\d+)"
severity_match = re.findall(severity_regex, contents)

confidence_regex = "Total issues .by confidence.:\s*(.*)Undefined: (\d+)\s*(.*)Low: (\d+)\s*(.*)Medium: (\d+)\s*(.*)High: (\d+)"
confidence_match = re.findall(confidence_regex, contents)

#print(severity_match[0])
#print(confidence_match[0])

def compare_banditscan_report():
    if severity_baseline_values == severity_match[0] and confidence_baseline_values == confidence_match[0]:
        exit(0)
    exit(1)

if __name__ == '__main__':
    print(compare_banditscan_report())


