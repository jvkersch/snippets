import React from 'react';
import { Col, Row } from 'react-bootstrap';


const simpleRow = (left, right) => {
    return <Row>
        <Col md={2}>{left}</Col>
        <Col md={10}>{right}</Col>
    </Row>
}

export default simpleRow;
