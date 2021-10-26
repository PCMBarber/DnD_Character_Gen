pipeline{
            agent any
            stages{
                    stage('--Front End--'){
                            steps{
                                    sh '''
                                            image="stratcastor/frontend:build-$BUILD_NUMBER"
                                            docker build -t $image /var/lib/jenkins/workspace/$JOB_BASE_NAME/frontend
                                            docker push $image
                                            kubectl set image deployment/frontend frontend=$image
                                    '''
                            }
                    }  
                    stage('--Service1--'){
                            steps{
                                    sh '''
                                            image="stratcastor/rand1:build-$BUILD_NUMBER"
                                            docker build -t $image /var/lib/jenkins/workspace/$JOB_BASE_NAME/randapp1
                                            docker push $image
                                            kubectl set image deployment/service1 service1=$image
                                    '''
                            }
                    }
                    stage('--Service2--'){
                            steps{
                                    sh '''
                                            image="stratcastor/rand2:build-$BUILD_NUMBER"
                                            docker build -t $image /var/lib/jenkins/workspace/$JOB_BASE_NAME/randapp2
                                            docker push $image
                                            kubectl set image deployment/service2 service2=$image
                                    '''
                            }
                    }
                    stage('--Back End--'){
                            steps{
                                    sh '''
                                            image="stratcastor/backend:build-$BUILD_NUMBER"
                                            docker build -t $image /var/lib/jenkins/workspace/$JOB_BASE_NAME/backend
                                            docker push $image
                                            kubectl set image deployment/backend backend=$image
                                    '''
                            }
                    }
            }
    }
