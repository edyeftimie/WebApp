import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';

import {Navbar, Footer} from '../src/components/layout';
import { CombinedProvider } from './components/context';
import {Network} from '../src/components/network';
import {Home} from '../src/components/home'
import {Player, PlayersList} from '../src/components/player'
import {Chart} from '../src/components/chart'
import {Team, TeamsList} from '../src/components/team'
import { PlayerInfo } from './components/playerInfo'
import { TeamInfo } from './components/teamInfo'
import { BrowserRouter as Router, Route, Routes, BrowserRouter} from 'react-router-dom';
// import {FullFeaturedCrudGrid } from '../src/Test';

const root = ReactDOM.createRoot(document.getElementById('root'));

const initializeApp = async () => {
  root.render(
    <React.StrictMode>
      <BrowserRouter>
        <CombinedProvider>
        <Network />
        <Navbar />
        { PlayersList}
        { TeamsList }
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/player" element={<Player />} />
          <Route path="/player/:id" element={<PlayerInfo />} />
          <Route path="/team" element={<Team />} />
          <Route path="/team/:id" element={<TeamInfo />} />
          <Route path="/chart" element={<Chart />} />
        </Routes>
        <Footer />
        </CombinedProvider>
      </BrowserRouter>
    </React.StrictMode>
  );
};

initializeApp();
// npx json-server db.json --port 3004 
// npx json-server dbt.json --port 3004 
// npm start
// npx playwright test