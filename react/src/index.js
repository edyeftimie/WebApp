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
import { Login } from './components/login'
import withAuth from './components/protected'
import { BrowserRouter as Router, Route, Routes, BrowserRouter} from 'react-router-dom';
// import {FullFeaturedCrudGrid } from '../src/Test';

const root = ReactDOM.createRoot(document.getElementById('root'));
const AuthenticatedHome = withAuth(Home);
const AuthenticatedPlayer = withAuth(Player);
const AuthenticatedTeam = withAuth(Team);
const AuthenticatedChart = withAuth(Chart);
const AuthenticatedPlayerInfo = withAuth(PlayerInfo);
const AuthenticatedTeamInfo = withAuth(TeamInfo);

const initializeApp = async () => {
  root.render(
    <React.StrictMode>
      <BrowserRouter>
        <CombinedProvider>
        <Network />
        <Navbar />
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Login />} />
          <Route path="/home" element={<AuthenticatedHome/>} />
          <Route path="/player" element={<AuthenticatedPlayer />} />
          <Route path="/player/:id" element={<AuthenticatedPlayerInfo />} />
          <Route path="/team" element={<AuthenticatedTeam />} />
          <Route path="/team/:id" element={<AuthenticatedTeamInfo />} />
          <Route path="/chart" element={<AuthenticatedChart />} />
        </Routes>
        <Footer />
        </CombinedProvider>
      </BrowserRouter>
    </React.StrictMode>
  );
};

initializeApp();