export default function Panel({ image, dialogue, scene }) {
    return (
      <div className="relative">
        <img src={`http://localhost:8000${image}`} alt="Comic panel" className="w-full rounded" />
        <div className="absolute bottom-4 left-4 bg-black bg-opacity-70 text-white px-4 py-2 rounded">
          Scene:
          {scene}
        </div>
        <div className="absolute bottom-4 left-4 bg-black bg-opacity-70 text-white px-4 py-2 rounded">
          {dialogue}
        </div>
      </div>
    );
  }