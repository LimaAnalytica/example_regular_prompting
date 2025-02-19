import React from 'react';
import ReactMarkdown from 'react-markdown';

function ResponseDisplay({ response, modelType }) {
  if (!response) return null;

  return (
    <div className="response-display">
      <h2>Respuesta:</h2>
      {response.status === 'success' ? (
        <div className="response-content">
          {modelType === 'code' ? (
            <div className="code-block">
              <ReactMarkdown>{response.response}</ReactMarkdown>
            </div>
          ) : (
            <div>{response.response}</div>
          )}
        </div>
      ) : (
        <div className="response-error">
          Error: {response.message}
        </div>
      )}
    </div>
  );
}

export default ResponseDisplay;