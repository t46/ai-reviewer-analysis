import openreview
import csv

client = openreview.api.OpenReviewClient(
    baseurl='https://api2.openreview.net'
)
venue_id = 'ICLR.cc/2024/Conference'
venue_group = client.get_group(venue_id)
submission_name = venue_group.content['submission_name']['value']
submissions = client.get_all_notes(invitation=f'{venue_id}/-/{submission_name}', details='replies')

review_name = venue_group.content['review_name']['value']

reviews = [
    {
        'submission_id': s.number,
        'summary': note.content['summary']['value'],
        'soundness': note.content['soundness']['value'],
        'presentation': note.content['presentation']['value'],
        'contribution': note.content['contribution']['value'],
        'strengths': note.content['strengths']['value'],
        'weaknesses': note.content['weaknesses']['value'],
        'questions': note.content['questions']['value'],
        'flag_for_ethics_review': note.content['flag_for_ethics_review']['value'],
        'rating': note.content['rating']['value'],
        'confidence': note.content['confidence']['value'],
        'code_of_conduct': note.content['code_of_conduct']['value']
    }
    for s in submissions
    for reply in s.details['replies']
    if f'{venue_id}/{submission_name}{s.number}/-/{review_name}' in reply['invitations']
    for note in [openreview.api.Note.from_json(reply)]
]

# CSVファイルに保存する部分
csv_filename = 'iclr2024_reviews.csv'

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = reviews[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for review in reviews:
        writer.writerow(review)

print(f"Reviews have been saved to {csv_filename}")