import React from 'react';

export default function SearchBar({address, handleSearchChange, handleSearchClick, clicked}) {
  return (
    <section className="search">
        <input value={address} onChange={handleSearchChange} type="text" placeholder="Wallet address here..."/>
        <button onClick={handleSearchClick}>{clicked ? 'Analyzed!' : 'Analyze'}</button>
    </section>

  );
}
