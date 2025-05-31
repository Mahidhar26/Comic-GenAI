import Panel from './Panel';

export default function ComicViewer({ panels }) {
  return (
    <div className="grid grid-cols-1 gap-4 p-4">
      {panels.map((panel, idx) => (
        <Panel key={idx} image={panel.image} dialogue={panel.dialogue} scene={panel.scene} />
      ))}
    </div>
  );
}