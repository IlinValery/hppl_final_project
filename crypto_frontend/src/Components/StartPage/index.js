import React from "react"
import './style.css'
import {Container, Row, Col, Button} from 'reactstrap';
import Header from '../Header'
import './style.css'

export default class StartPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};

    }

    changeEndpoint(endpoint) {
        window.location = '/' + endpoint
    }

    render() {
        return (
            <Container >
                <Header text={this.props.text}/>
                <Container >

                        <Row className="main-container">
                            <Col sm={12} className="class-col">

                                <Button
                                    size='lg'
                                    onClick={() => this.changeEndpoint('encrypt')}
                                    color="secondary">
                                    Encrypt
                                </Button>{' '}
                            </Col>
                            <Col>
                                <br/>
                            </Col>
                            <Col sm={12} className="class-col">

                                <Button
                                    size='lg'
                                    onClick={() => this.changeEndpoint('decrypt')}
                                    color="secondary">
                                    Decrypt
                                </Button>{' '}
                            </Col>
                        </Row>
                </Container>
            </Container>
        );
    }
}