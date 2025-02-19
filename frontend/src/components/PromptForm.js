import React from 'react';

function PromptForm({ onSubmit }) {
  const [prompt, setPrompt] = React.useState('');
  const [modelType, setModelType] = React.useState('general');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ prompt, model_type: modelType });
  };

  return (
    <form onSubmit={handleSubmit} className="prompt-form">
      <div className="form-group">
        <label htmlFor="model-type">Modelo:</label>
        <select
          id="model-type"
          value={modelType}
          onChange={(e) => setModelType(e.target.value)}
        >
          <option value="general">General</option>
          <option value="spanish">Español</option>
          <option value="code">Código</option>
        </select>
      </div>
      <div className="form-group">
        <label htmlFor="prompt">Prompt:</label>
        <textarea
          id="prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Escribe tu prompt aquí..."
          rows="4"
        />
      </div>
      <button type="submit">Enviar</button>
    </form>
  );
}

export default PromptForm;