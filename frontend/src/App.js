import React from 'react';
import Editor from './components/Editor';
import Toolbar from './components/Toolbar';
import Sidebar from './components/Sidebar';
import Home from './pages/Home';

const App = () => {
  return (
    <div className="app-container flex">
      <Sidebar />
      <div className="main-content flex-1 p-4">
        {/* Toolbar could be placed here if needed */}
        <Home />
      </div>
    </div>
  );
};

export default App;
