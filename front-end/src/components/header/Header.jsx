import React from 'react';

export default function Header({handleMetaMaskClick, user}) {
  return (
    <header className='header'>
        <h1>C<span id="blue">h</span></h1>
        <p onClick={handleMetaMaskClick}>{user}</p>
    </header>
)
}
