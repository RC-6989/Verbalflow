import React from 'react';
import WebcamCapture from './components/WebcamCapture';

const App: React.FC = () => {
  return (
    <div className="App">
      <h1 className="text-center text-2xl font-bold my-6">verbalflow</h1>
      <WebcamCapture />
    </div>
  );
};

export default App;
