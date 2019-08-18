import React, { Component } from 'react';
import Issue from './Issue';
import { Container, Row, Col } from 'react-bootstrap';
import { LeftCol, RightCol } from './SimpleCol';

import axios from 'axios';

import './Issues.css';

class Issues extends Component {

    state = {
        issues: null
    }

    componentDidMount() {
        axios.get(" https://api.github.com/repos/pandas-dev/pandas/issues").then(
            result => {
                const issues = result.data.map(
                    entry => {
                        return {
                            title: entry.title,
                            body: entry.body,
                            number: entry.number,
                            avatar_url: entry.user.avatar_url
                        }
                    });

                this.setState({
                    issues: issues
                });
            }
        );
    }

    render() {
        let issueBodies = null;
        if (!this.state.issues) {
            issueBodies = <Col>Loading</Col>;
        } else {
            issueBodies = this.state.issues.map(
                issue => <Issue
                    title={issue.title}
                    issueText={issue.body}
                    key={issue.number}
                    avatar_url={issue.avatar_url} />
            );
        }

        return (
            <Container>
                <Row className="m-3">
                    <LeftCol></LeftCol>
                    <RightCol>
                        <h2 className="text-left repo-title">{this.props.repo}</h2>
                    </RightCol>
                </Row>
                {issueBodies}
            </Container>);

    }
}

export default Issues;
