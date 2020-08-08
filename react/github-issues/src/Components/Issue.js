import React, { Component } from 'react';
import { Row, Col } from 'react-bootstrap';
import ReactMarkdown from 'react-markdown';

import './Issue.css';
import { LeftCol, RightCol } from './SimpleCol';


class Issue extends Component {



    render() {
        return <Row className="issue m-3">
            <Col>
                <Row>
                    <LeftCol></LeftCol>
                    <RightCol>
                        <h3 className="text-left issue-title pb-2">{this.props.title}</h3>
                    </RightCol>
                </Row>
                <Row>
                    <LeftCol>
                        <img className="avatar" width={128} height={128} src={this.props.avatar_url} />
                    </LeftCol>
                    <RightCol>
                        <div className="text-left">
                            <ReactMarkdown source={this.props.issueText} />
                        </div>
                    </RightCol>
                </Row>
            </Col>
        </Row>
    }
}


export default Issue;
