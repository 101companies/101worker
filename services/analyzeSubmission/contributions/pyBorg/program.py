class Borg(object):

    __state = {}
    def __init__(self):
        self.__dict__ = Borg.__state
        
class Company(Borg):
    
    def __init__(self, name, subunits):
        Borg.__init__(self)
        self.name = name
        self.subunits = subunits
      
    def cut(self):
        for s in self.subunits:
            s.cut()
            
    def total(self):
        return sum(map(lambda s: s.total(), self.subunits))
        
class Department(object):
    
    def __init__(self, name, manager, subunits):
        self.name = name
        self.manager = manager
        self.subunits = subunits

    def cut(self):
        self.manager.cut()
        for s in self.subunits:
            s.cut()
       
    def total(self):
        return self.manager.total() + sum(map(lambda s: s.total(), self.subunits))
        
class Employee(object):

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        
    def cut(self):
        self.salary /= 2
        
    def total(self):
        return self.salary
       

if __name__ == '__main__':
    company = Company(
    "Meganalysis",
    [
        Department(
            "Research",
            Employee(
                name = "Craig",
                salary = 123456.0
            ),
            subunits = [
                Employee(
                    name = "Erik",
                    salary = 12345.0
                ),
                Employee(
                    name = "Ralf",
                    salary = 1234.0
                )
            ]
        ),
        Department(
            name = "Development",
            manager = Employee(
                name = "Ray",
                salary = 234567.0
            ),
            subunits = [
                Department(
                    name = "Dev1",
                    manager = Employee(
                        name = "Klaus",
                        salary = 23456.0
                    ),
                    subunits = [
                        Department(
                            name = "Dev1.1",
                            manager = Employee(
                                name = "Karl",
                                salary = 2345.0
                            ),
                            subunits = [
                                Employee(
                                    name = "Joe",
                                    salary = 2344.0
                                )
                            ]
                        )
                    ]
                )
            ]
        )            
    ]
)
    first_total = company.total()
     
    company2 = Company(
        "Meganalysis",
        [
            Department(
                "Research",
                Employee(
                    name = "Craig",
                    salary = 123456.0
                ),
                subunits = [
                    Employee(
                        name = "Erik",
                        salary = 12345.0
                    ),
                    Employee(
                        name = "Ralf",
                        salary = 1234.0
                    )
                ]
            ),
            Department(
                name = "Development",
                manager = Employee(
                    name = "Ray",
                    salary = 234567.0
                ),
                subunits = [
                    Department(
                        name = "Dev1",
                        manager = Employee(
                            name = "Klaus",
                            salary = 23456.0
                        ),
                        subunits = [
                            Department(
                                name = "Dev1.1",
                                manager = Employee(
                                    name = "Karl",
                                    salary = 2345.0
                                ),
                                subunits = [
                                    Employee(
                                        name = "Joe",
                                        salary = 2344.0
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )            
        ]
    )
    
    company2.cut()
    assert company.total() * 2.0 == first_total
