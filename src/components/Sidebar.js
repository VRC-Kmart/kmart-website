import React from 'react';
import config from '../config';
import KmartEssentials from './KmartEssentials';
const SideBar = () => {
  return (
    <div className="side-bar">
      <img src={config.logo} className="logo" alt="logo" />
      <ul className="side-bar-list">
        <button>Extra Credit</button>
        <button>Find Us</button>
        <button>Sale Circular</button>
        <button>About Kmart</button>
        <button>Headlines</button>
        <button>Comments</button>
        <button>Window Shop</button>
        <KmartEssentials />
      </ul>
    </div>
  );
}

export default SideBar;
