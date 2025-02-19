// frontend/src/App.js
import React, { useState } from 'react';
import PromptForm from './components/PromptForm';
import ResponseDisplay from './components/ResponseDisplay';
import './App.css';

// Definir la URL del backend como una constante
const BACKEND_URL = 'http://localhost:8000';

function App() {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [currentModelType, setCurrentModelType] = useState('general'); // Añadir este estado

  const handlePromptSubmit = async (promptData) => {
    try {
      console.log('Sending request to:', `${BACKEND_URL}/api/prompt`);
      console.log('Request data:', promptData);

      // Actualizar el modelo actual
      setCurrentModelType(promptData.model_type);

      const res = await fetch(`${BACKEND_URL}/api/prompt`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: promptData.prompt,
          model_type: promptData.model_type === 'spanish' ? 'spanish' : 'general'
        }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      console.log('Response data:', data);
      setResponse(data);
      setError(null);
    } catch (error) {
      console.error('Error:', error);
      setError(`Error en la API: ${error.message}`);
      setResponse(null);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Hugging Face Prompting</h1>
      </header>
      <main>
        <PromptForm onSubmit={handlePromptSubmit} />
        {error && <div className="error-message">{error}</div>}
        <ResponseDisplay response={response} modelType={currentModelType}/>
      </main>
    </div>
  );
}

export default App;