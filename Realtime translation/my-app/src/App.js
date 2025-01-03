import React from "react";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { PuffLoader } from "react-spinners";

export default function App() {
  // Extract the speech recognition states & methods
  const { transcript, resetTranscript, listening } = useSpeechRecognition();

  // If speech recognition is not supported, bail out
  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return <div>Your browser doesn't support speech recognition.</div>;
  }

  // Toggle microphone on/off
  const handleMicrophoneToggle = () => {
    if (listening) {
      SpeechRecognition.stopListening();
      toast.error("Microphone Off", { autoClose: 1500 });
    } else {
      SpeechRecognition.startListening({ continuous: true });
      toast.success("Microphone On", { autoClose: 1500 });
    }
  };

  // Reset the transcript
  const handleReset = () => {
    resetTranscript();
    toast.info("Transcript reset", { autoClose: 1500 });
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        margin: "0 auto",
        maxWidth: "600px",
        padding: "20px",
      }}
    >
      <h2 style={{ marginBottom: "1rem" }}>React Speech To Text</h2>

      {/* Display recognized text or a placeholder */}
      <p 
        style={{ 
          border: "1px solid #ccc", 
          padding: "1rem", 
          width: "100%", 
          minHeight: "80px",
          borderRadius: "8px",
          backgroundColor: "#f8f9fa"
        }}
      >
        {transcript || "Press the microphone button and start speaking."}
      </p>

      {/* Show loader if currently listening */}
      <div style={{ margin: "1rem 0", minHeight: "40px" }}>
        {listening && (
          <PuffLoader
            size={40}
            color="#3498db"
            loading={listening}
          />
        )}
      </div>

      {/* Control buttons */}
      <div style={{ display: "flex", gap: "1rem" }}>
        <button
          onClick={handleMicrophoneToggle}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: listening ? "#e53e3e" : "#38a169",
            color: "#fff",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            transition: "background-color 0.2s",
            fontSize: "16px"
          }}
        >
          {listening ? "Stop" : "Start"}
        </button>

        <button
          onClick={handleReset}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: "#4a5568",
            color: "#fff",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            transition: "background-color 0.2s",
            fontSize: "16px"
          }}
        >
          Reset
        </button>
      </div>

      {/* Toast Container for notifications */}
      <ToastContainer 
        position="bottom-right"
        autoClose={1500}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </div>
  );
}
