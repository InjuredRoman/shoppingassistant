import logo from './geeves.webp';
import './ATL.css';
import { useState } from "react";
import { Paperclip, Send } from "lucide-react";

function App() {
  const [query, setQuery] = useState("");
  const [files, setFiles] = useState([]);

  const handleFileChange = (e) => {
    if (!e.target.files) return;
    setFiles([...files, ...Array.from(e.target.files)]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // make form data from query and image(s)
    const formData = new FormData();
    formData.append("query", query)
    files.forEach(f => {
      formData.append("files", f)
    })
    console.log(formData);

    // send it!
    const res = fetch("http://127.0.0.1:8000/query", {
      method: "POST",
      body: formData,
    }).then(res => {
      console.log(res.json)
    });
    // and reset format
    setQuery("");
    setFiles([]);
  };
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
      </header> */}
  return (
    <div className="App">

      <div className="flex items-center">
        {/*  grid grid-cols-3">*/ }
        {/* <div className="block">
          <img src={logo} className="App-logo" alt="logo" />
        </div> */}
        {/* <div className="block"> */}

        <form
        onSubmit={handleSubmit}
        className="float-end flex items-center gap-2 rounded-2xl border border-gray-300 bg-white px-3 py-2 shadow-sm focus-within:ring-2 focus-within:ring-blue-500"
      >
        {/* File Upload */}
        <label className="cursor-pointer text-gray-500 hover:text-gray-700">
          <Paperclip size={20} />
          <input
            type="file"
            multiple
            onChange={handleFileChange}
            className="hidden"
          />
        </label>

        {/* Text Input */}
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type your message..."
          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          // className="flex-1 bg-transparent text-sm outline-none placeholder-gray-400"
        />

        {/* Submit Button */}
        <button
          type="submit"
          className="rounded-full bg-blue-500 p-2 text-white hover:bg-blue-600 transition-colors"
        >
          <Send size={18} />
        </button>
        </form>
        </div>
        {/* <div className="block">
          <img src={logo} className="App-logo" alt="logo" />
        </div> */}
      {/* </div> */}
    </div>
  );
}

export default App;
