import React, { useState, useEffect } from "react";
import axios from "axios";
import { FaUpload, FaFileAlt } from "react-icons/fa";
import "./SideBar.css";

const baseURL = process.env.REACT_APP_API_BASE_URL;

export default function SideBar() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = () => {
    axios
      .get(`${baseURL}/files`)
      .then((response) => {
        setFiles(response.data.files);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    if (!selectedFile) {
      setUploadStatus("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    axios
      .post(`${baseURL}/uploadfile`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        setUploadStatus("File uploaded successfully!");
        setFiles([...files, response.data.filename]);
        setSelectedFile(null);
      })
      .catch((error) => {
        console.log(error);
        setUploadStatus("File upload failed. Please try again.");
      });
  };

  const handleFileDelete = (file) => {
    console.log(file);
    axios
      .post(`${baseURL}/deletefile`, { prefix: file })
      .then((response) => {
        setFiles(files.filter((f) => f !== file));
        console.log(response.data.detail);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div className="sidebar">
      <h2>Files</h2>
      <ul className="fileList">
        {files.map((file, index) => (
          <li key={index} className="fileItem">
            {file}
            <button
              className="deleteButton"
              onClick={() => handleFileDelete(file)}
            >
              X
            </button>
          </li>
        ))}
      </ul>
      <div className="uploadSection">
        <label htmlFor="fileInput" className="fileInputLabel">
          <FaFileAlt className="icon" />
          {selectedFile ? selectedFile.name : "Choose File"}
        </label>
        <input
          id="fileInput"
          type="file"
          className="fileInput"
          onChange={handleFileChange}
        />
        <button className="uploadButton" onClick={handleFileUpload}>
          <FaUpload className="icon" />
          Upload File
        </button>
        <p className="uploadStatus">{uploadStatus}</p>
      </div>
    </div>
  );
}
