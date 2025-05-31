import { useState } from 'react';
import ComicInput from './components/ComicInput';
import ComicViewer from './components/ComicViewer';

function App() {
  const [panels, setPanels] = useState([]);

  return (
    <div>
      <h1 className="text-3xl p-4">Comic Generator</h1>
      <ComicInput onPanelsReady={setPanels} />
      <ComicViewer panels={panels} />
    </div>
  );
}

export default App;