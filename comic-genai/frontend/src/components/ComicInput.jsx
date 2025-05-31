import { useState } from 'react';
import axios from 'axios';

export default function ComicInput({ onPanelsReady }) {
  const [text, setText] = useState('');

  const handleSubmit = async () => {
    const storyboardRes = await axios.post('http://localhost:8000/storyboard', {
      text,
      panel_count: 4,
    });

    const generateRes = await axios.post('http://localhost:8000/generate-comic', {
      panels: storyboardRes.data.panels
    });

    const combined = storyboardRes.data.panels.map((panel, index) => ({
      ...panel,
      image: generateRes.data.images[index]
    }));

    onPanelsReady(combined);
  };

  return (
    <div className="p-4">
      <textarea
        className="w-full p-2 border"
        rows={3}
        placeholder="Write a short story line..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={handleSubmit} className="mt-2 px-4 py-2 bg-blue-600 text-white">
        Generate Comic
      </button>
    </div>
  );
}