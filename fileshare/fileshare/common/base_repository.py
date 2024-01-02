import json, uuid
from decimal import Decimal

class Repository():

    def __init__(self, session):
        self.session = session
        #Each repository should define its model_type
        self.model_type = None

    def get(self,m_id):
        """Get model from db 

        Args:
            model_type (Type of Model): Classname of model
            id (integer): id of the entity

        Returns:
            model: model 
        """
        with self.session as session:       
            return session.query(self.model_type).filter_by(id=m_id).first()
        # return self.session.query(self.model_type).filter_by(id=m_id).first()

    def get_all(self, limit=1000, offset=0):
        """Get all models from db 


        Returns:
            model_list: list of models
        """
        with self.session as session:       
            return session.query(self.model_type).limit(limit).offset(offset).all()
        # return self.session.query(self.model_type).limit(limit).offset(offset).all()

    def add(self, model):
        """Add model to db

        Args:
           model : model to be added to db

        Returns:
            model: model 
        """              
        self.session.add(model)
        self.session.commit()
        return model
    
    def update(self,id,model):
        """Commit changes to models
        """
        self.session.query(self.model_type).filter_by(id=id).update(model)      
        self.session.commit()
    
    def remove(self, m_id):
        """Remove mode from db

        Args:
            model_type (Type of Model): Classname of model
            id (integer): id of the entity
        """        
        self.session.query(self.model_type).filter_by(id=m_id).delete()
        self.session.commit()
