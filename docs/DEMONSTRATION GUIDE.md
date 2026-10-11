# One-minute demonstration guide

Student: Hammad Kashif | P24-0631 | BCS-5C

The video must not exceed 60 seconds. This is a recording plan, not a completed video.

## Prepare before recording

1. Start MySQL and `backend/app.py`. Have the server terminal visible for the opening.
2. Open http://127.0.0.1:5000 in the browser.
3. Import the supplied Postman collection, run it once to check the assertions, then prepare to rerun it during the video. Complete cleanup after practice.
4. Prepare a short title, faculty, skills and description so typing is quick. Keep the browser and Postman side by side if possible.
5. Enable a screen recorder (e.g. Windows Snipping Tool screen recording or OBS) and select only the needed windows. Do not show `.env` or passwords.

## Suggested 58-second sequence

| Time | Action and narration |
| --- | --- |
| 0-5 sec | Show backend terminal and browser. Say: "Hammad Kashif, P24-0631. This is my MySQL-backed Research Opportunity Portal." |
| 5-18 sec | Click Post opportunity, fill all fields, and save. "Creating an opportunity stores it through the REST API." |
| 18-25 sec | Show the new card and open Details. "Stored opportunities and complete details load from MySQL." |
| 25-33 sec | Edit the title or positions and save. "The update is saved and reflected on the page." |
| 33-38 sec | Click Close and show the Closed badge. "Faculty can close an opening." |
| 38-44 sec | Delete and confirm. Show that the card disappears. |
| 44-58 sec | Switch to Postman. Run the numbered collection and show the requests, responses and passing assertions, including deleted ID = 404 and invalid body = 400. |

If the run takes longer, record the collection run first and leave the results ready to show. The video should visibly include API request and response bodies in Postman, not only a generic test summary.

Save as `docs/demonstration.mp4`, or upload the video and add the accessible link to README.md. Verify the final duration and instructor access before submission.
