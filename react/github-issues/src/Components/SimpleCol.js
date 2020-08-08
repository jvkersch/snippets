import React from 'react';
import { Col } from 'react-bootstrap';


const LeftCol = (props) => {
    return <Col md={2}>
        {props.children}
    </Col>;
}


const RightCol = (props) => {
    return <Col md={10}>
        {props.children}
    </Col>;
}

export { LeftCol, RightCol };
