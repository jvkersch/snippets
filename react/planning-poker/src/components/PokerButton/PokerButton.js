import React from 'react';

const pokerButton = (props) => {
    return <button onclick={props.onClick}>
        {props.score}
    </button>
}

export default pokerButton;
