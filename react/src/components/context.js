import React, { createContext, useContext, useState } from 'react';

const CombinedContext = createContext();

export function CombinedProvider({ children }) {
    const [playersList, setPlayersList] = useState([]);
    const [teamsList, setTeamsList] = useState([]);

    return (
        <CombinedContext.Provider value={{ playersList, setPlayersList, teamsList, setTeamsList }}>
        {/* <CombinedContext.Provider value={{ playersList, setPlayersList}}> */}
            {children}
        </CombinedContext.Provider>
    );
};

export const useCombinedContext = () => useContext(CombinedContext);