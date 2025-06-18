import { useState } from 'react';

export default function ComicApp() {
  const [comic, setComic] = useState(null);
  const [panels, setPanels] = useState([]);
  const [scenePrompt, setScenePrompt] = useState('');
  const [imageMap, setImageMap] = useState({});
  const [loading, setLoading] = useState(false);

  const handleComicCreate = (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    const name = form.get('name');
    const desc = form.get('desc');
    const context = form.get('context');
    const count = parseInt(form.get('count'));
    if (count > 10) return alert('Maximum 10 panels supported');
    setComic({ name, desc, context, count });
    setPanels(Array(count).fill(null));
  };

  const handleSceneGenerate = async (i) => {
    if (!scenePrompt) return;
    try {
      setLoading(true);
      const res = await fetch('http://localhost:8000/generate-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scene: scenePrompt })
      });
      const data = await res.json();
      const newPanels = [...panels];
      newPanels[i] = { name: `Scene ${i + 1} `, prompt: scenePrompt, image: data.image };
      setPanels(newPanels);
      setImageMap({ ...imageMap, [i]: data.image });
      setScenePrompt('');
    } catch (err) {
      console.error('Scene generation failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDrag = (e, idx) => {
    e.dataTransfer.setData('drag-idx', idx);
  };

  const handleDrop = (e, idx) => {
    const dragIdx = e.dataTransfer.getData('drag-idx');
    if (dragIdx === null) return;
    const newPanels = [...panels];
    const [dragItem] = newPanels.splice(dragIdx, 1);
    newPanels.splice(idx, 0, dragItem);
    setPanels(newPanels);
  };

  return (
    <div className="comic-app">
      <style>{`
        .comic-app {
          font-family: 'Segoe UI', sans-serif;
          background: linear-gradient(to right, #f9fafb, #e0f2fe);
          min-height: 100vh;
          padding: 2rem;
          box-sizing: border-box;
        }

        .comic-form {
          max-width: 500px;
          margin: 0 auto;
          background: white;
          padding: 2rem;
          border-radius: 12px;
          box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }

        .comic-form h1 {
          font-size: 28px;
          margin-bottom: 20px;
          text-align: center;
        }

        .comic-form input,
        .comic-form textarea {
          width: 100%;
          margin-bottom: 15px;
          padding: 10px;
          font-size: 16px;
          border: 1px solid #ccc;
          border-radius: 8px;
        }

        .comic-form button {
          width: 100%;
          padding: 12px;
          font-size: 16px;
          font-weight: bold;
          background: #0ea5e9;
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
        }

        .comic-panel-editor {
          display: flex;
          gap: 2rem;
        }

        .sidebar {
          width: 250px;
          background: #1e293b;
          color: white;
          padding: 1rem;
          border-radius: 12px;
          height: fit-content;
        }

        .sidebar h2 {
          font-size: 20px;
          margin-bottom: 8px;
        }

        .scene-box {
          padding: 10px;
          margin: 6px 0;
          background: #334155;
          border-radius: 6px;
          cursor: grab;
          text-align: center;
        }

        .panel-generator {
          flex: 1;
          background: white;
          border-radius: 12px;
          padding: 2rem;
          box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        }

        .scene-input {
          width: 100%;
          min-height: 80px;
          padding: 10px;
          font-size: 15px;
          border-radius: 8px;
          border: 1px solid #ccc;
          margin-bottom: 20px;
        }

        .panel-buttons {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
          margin-bottom: 20px;
        }

        .panel-buttons button {
          flex: 1 1 150px;
          padding: 10px;
          background-color: #0ea5e9;
          border: none;
          color: white;
          border-radius: 8px;
          font-weight: bold;
          cursor: pointer;
        }

        .generated-images {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
          gap: 20px;
        }

        .image-container img {
          width: 100%;
          border-radius: 10px;
          border: 2px solid #ccc;
        }

        @media (max-width: 768px) {
          .comic-panel-editor {
            flex-direction: column;
          }

          .sidebar {
            width: 100%;
          }
        }
      `}</style>

      {!comic ? (
        <form className="comic-form" onSubmit={handleComicCreate}>
          <h1>Create a Comic</h1>
          <input name="name" placeholder="Comic Name" required />
          <textarea name="desc" placeholder="Short Description" required />
          <input name="context" placeholder="Context (e.g., medieval fantasy)" required />
          <input name="count" type="number" placeholder="Number of Panels (max 10)" required />
          <button type="submit">Create</button>
        </form>
      ) : (
        <div className="comic-panel-editor">
          <div className="sidebar">
            <h2>{comic.name}</h2>
            <p>{comic.desc}</p>
            <div className="scene-list">
              {panels.map((panel, i) => (
                <div
                  key={i}
                  className="scene-box"
                  draggable
                  onDragStart={(e) => handleDrag(e, i)}
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) => handleDrop(e, i)}
                >
                  {panel ? panel.name : `Scene ${i + 1}`}
                </div>
              ))}
            </div>
          </div>

          <div className="panel-generator">
            <h3>Generate Scene</h3>
            <textarea
              className="scene-input"
              value={scenePrompt}
              onChange={(e) => setScenePrompt(e.target.value)}
              placeholder="Enter a prompt for this panel"
            />
            <div className="panel-buttons">
              {panels.map((_, i) => (
                <button key={i} onClick={() => handleSceneGenerate(i)} disabled={loading}>
                  {loading ? `Loading...` : `Generate Scene ${i + 1}`}
                </button>
              ))}
            </div>
            <div className="generated-images">
              {panels.map((panel, i) =>
                panel?.image ? (
                  <div key={i} className="image-container">
                    <img src={"http://localhost:8000${panel.image}"} alt={"Scene ${}"} />
                  </div>
                ) : null  )}
            </div>
          </div>
        </div>
      )
    }
    </div>
    )
}