import { useState, useRef } from "react";
import "./App.css";

function App() {
  const [note, setNote] = useState("");
  const [notes, setNotes] = useState([]);
  const [editIndex, setEditIndex] = useState(null);
  const inputRef = useRef(null);

  const handleAdd = () => {
    if (!note.trim()) 
      return;

    if (editIndex !== null) {
      const updated = [...notes];
      updated[editIndex] = note;
      setNotes(updated);
      setEditIndex(null);
    } else {
      setNotes([...notes, note]);
    }

    setNote("");
    inputRef.current.focus();
  };

  const handleDelete = (index) => {
    setNotes(notes.filter((_, i) => i !== index));
  };

  const handleUpdate = (index) => {
    setNote(notes[index]);
    setEditIndex(index);
    inputRef.current.focus();
  };

  return (
    <div className="container">
      <h1>Note App</h1>

      <div className="input-box">
        <input
          ref={inputRef}
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="Write a note..."
        />
        <button onClick={handleAdd}>
          {editIndex !== null ? "Update" : "Add"}
        </button>
      </div>

      <div className="list-box">
        {notes.map((n, i) => (
          <div key={i} className="note item">
            <span>{n}</span>

            <div className="actions">
              <button onClick={() => handleUpdate(i)}>Update</button>
              <button onClick={() => handleDelete(i)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;