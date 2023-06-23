

import {BrowserRouter as Router, Route,Routes} from 'react-router-dom'

import Home from './Home'
import Player from './Player'
import Socket from './Socket';
function App() {
  
  return (
    <Router>
    <div className="App">
    
      <div className="content">
        <Routes>
          <Route exact path="/" element={<Home/>}/>
        </Routes>
        <Routes>
          <Route exact path="/player" element={<Player/>}/>        
        </Routes>
        <Routes>
          <Route exact path="/socket" element={<Socket/>}/>        
        </Routes>
      </div>
    </div>
    </Router>
  );
}
export default App;
