async function postCommentToGitHub(comment_body, commit_id, file_path, start_line, line, start_side, side) {
  const { Octokit } = await import('@octokit/core');
  const fetch = require('node-fetch');

  try {
    const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN, request: { fetch }});

    comment_body = comment_body.replace(/\\n/g, '\n').replace(/\\t\+/g, '    ');

    console.log('Arguments:', { comment_body, commit_id, file_path, start_line, line, start_side, side });

    const [owner, repo] = process.env.GITHUB_REPOSITORY.split('/');
    const pull_number = process.env.GITHUB_EVENT_NUMBER;

    // console.log('Repository Info:', { owner, repo, pull_number });
    console.log(comment_body);

    let response;
    if (start_line == line) {
      response = await octokit.request('POST /repos/{owner}/{repo}/pulls/{pull_number}/comments', {
          owner,
          repo,
          pull_number,
          commit_id,
          path: file_path,
          body: comment_body,
          line: parseInt(line),
          side
        });
    } else {
      response = await octokit.request('POST /repos/{owner}/{repo}/pulls/{pull_number}/comments', {
          owner,
          repo,
          pull_number,
          commit_id,
          path: file_path,
          body: comment_body,
          start_line: parseInt(start_line),
          line: parseInt(line),
          start_side,
          side
        });
    }

    if (response.status !== 201) {
      throw new Error(`GitHub API responded with ${response.status}: ${response.statusText}`);
    }

    console.log('Comment posted successfully:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error posting comment:', error.message);
    console.error(error);
  }
}

const args = process.argv.slice(2);

if (args.length < 7) {
  console.error('Insufficient arguments. Expected: comment_body, commit_id, file_path, start_line, line, start_side, side');
  process.exit(1);
}

const [comment_body, commit_id, file_path, start_line, line, start_side, side] = args;

const formatted_comment_body = comment_body.replace(/\\n/g, '\n').replace(/\\t\+/g, '    ');

postCommentToGitHub(formatted_comment_body, commit_id, file_path, start_line, line, start_side, side)
  .then(response => console.log('Comment posted successfully:', response))
  .catch(error => console.error('Error posting comment:', error));
 
