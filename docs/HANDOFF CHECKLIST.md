# Handoff and final submission checklist

Prepared for Hammad Kashif, P24-0631, BCS-5C.

## Work already included

- Complete Python backend and HTML/CSS/JavaScript frontend.
- MySQL schema, configuration template and setup instructions.
- Exported Postman collection with ordered requests and assertions.
- Automated API tests and verification notes.
- Real local development history in the accompanying Git bundle.
- Short recording plan.

## Tasks for your friend

1. Extract the ZIP and run the application using README.md.
2. Import and run the Postman collection in Postman.
3. Record the video, maximum 60 seconds, using DEMONSTRATION GUIDE.md.
4. Create a GitHub repository in your intended account. Keep it accessible to the instructor.
5. Preserve the supplied development history. From the extracted ZIP directory:

```powershell
git clone development-history.bundle research-opportunity-portal
Set-Location research-opportunity-portal
# Replace YOUR_ACCOUNT with the actual GitHub account and use the repo you created.
git remote remove origin
git remote add origin https://github.com/YOUR_ACCOUNT/research-opportunity-portal.git
```

The clone contains the complete committed project. It avoids reconstructing or inventing development commits. Keep the extracted source folder as a reference. Configure Git with your own name and email for new commits.

6. Edit README.md: put the real GitHub repository URL in the repository line. Add `docs/demonstration.mp4` or a real video link. Add the recorded video to the cloned project if using a file. GitHub may reject very large video files, so a video link is acceptable.
7. Commit the final additions and publish:

```powershell
git add README.md docs
git commit -m "Add repository link and final demonstration"
git push -u origin main
```

8. Build the final ZIP from the project folder (exclude `.git`, `.env`, `.venv`, cache files and installed packages). Include frontend/backend source, schema, Postman collection, README with the repository link, and the recorded video or video link.
9. Use the required submission filename: `P24_0631_Hammad_Kashif_BCS-5C.zip`.
10. Open the final ZIP and verify the project files, repository link and video/video link before submitting.

Do not publish `.env`, local database passwords, personal access tokens, installed dependencies or the temporary MySQL testing files. The provided handoff ZIP excludes those items. GitHub publication and recording remain intentionally unfinished per the user's request.

