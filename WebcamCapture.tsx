import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';

const WebcamCapture: React.FC = () => {
  const webcamRef = useRef<Webcam>(null);
  const [image, setImage] = useState<string | null>(null);
  const [cameraOn, setCameraOn] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);

  const capture = () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    setImage(imageSrc || null);
  };

  const handleTurnOnCamera = () => {
    setLoading(true);
    setTimeout(() => {
      setCameraOn(true);
      setLoading(false);
    }, 800); // Simulated camera load time
  };

  return (
    <div className="WebcamCapture">
      <h2 className="text-3xl font-bold">prepare for your interview</h2>

      {loading ? (
        <div className="loader"></div> // Loader animation
      ) : cameraOn ? (
        image ? (
          <div>
            <img src={image} alt="Captured" className="rounded-md shadow-lg mb-4" />
            <button 
              onClick={() => setImage(null)} 
              className="bg-red-500 text-white p-3 rounded-lg transition-all hover:bg-red-600">
              Retake Photo
            </button>
          </div>
        ) : (
          <>
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              className="rounded-md shadow-lg"
            />
            <button 
              onClick={capture} 
              className="mt-4 bg-green-500 text-white p-3 rounded-lg transition-all hover:bg-green-600">
              Capture Photo
            </button>
          </>
        )
      ) : (
        <button 
          onClick={handleTurnOnCamera} 
          className="turn-on-camera mt-6 p-4 text-lg">
          turn camera on
        </button>
      )}
    </div>
  );
};

export default WebcamCapture;
